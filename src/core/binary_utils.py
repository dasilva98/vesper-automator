import struct
import os
import logging
from datetime import datetime

logger = logging.getLogger("vesper_automator")

def bcd_to_int(byte_val):
    """Helper: Converts a binary-coded decimal (BCD) byte to an integer."""
    return (byte_val // 16) * 10 + (byte_val % 16)

def read_vesper_header(filepath):
    """
    Reads the standard 150-byte Vesper header.
    Returns a dictionary with raw common fields (IDs, SampleRate, Time, Configs).
    """
    HEADER_SIZE = 150
    if not os.path.exists(filepath):
        return None

    with open(filepath, 'rb') as f:
        header = f.read(HEADER_SIZE)

    # 1. Decode IDs
    device_id = struct.unpack('<I', header[4:8])[0]
    try:
        sensor_name = header[8:24].split(b'\x00')[0].decode('ascii')
    except:
        sensor_name = "Unknown"

    # 2. Decode Basic Configs
    sample_rate = struct.unpack('<I', header[28:32])[0]
    bitmask = struct.unpack('<I', header[40:44])[0]

    # 3. Decode Extended Configs (Offsets 44, 48, 52, 56)
    # We read 4 unsigned integers (I) in Little Endian (<)
    config0 = struct.unpack('<I', header[44:48])[0]
    config1 = struct.unpack('<I', header[48:52])[0]
    config2 = struct.unpack('<I', header[52:56])[0]
    config3 = struct.unpack('<I', header[56:60])[0]

    # 4. Decode BCD Timestamp
    try:
        h = bcd_to_int(header[132])
        m = bcd_to_int(header[133])
        s = bcd_to_int(header[134])
        month = bcd_to_int(header[137])
        day   = bcd_to_int(header[138])
        year  = 2000 + bcd_to_int(header[139])
        start_dt = datetime(year, month, day, h, m, s)
    except ValueError:
        start_dt = datetime.fromtimestamp(os.path.getmtime(filepath))

    return {
        "DeviceID": f"{device_id:X}",
        "Sensor": sensor_name,
        "SampleRate": sample_rate,
        "Bitmask": bitmask,
        "Config0": config0,
        "Config1": config1,
        "Config2": config2,
        "Config3": config3,
        "Start_Time": start_dt
    }

def generate_metadata_file(filepath, meta):
    """
    Generates the sidecar .txt file required to replace VesperApp.
    Formats Configs and Bitmask as Hexadecimal to match Vesper output.
    """
    txt_path = os.path.splitext(filepath)[0] + ".txt"
    
    lines = [
        f"DeviceID:{meta['DeviceID']}",
        "HWID:0", # TODO We need to find this byte
        "FWID:112", # TODO We need to find this byte
        f"Sensor:{meta['Sensor']}",
        f"SampleRate:{meta['SampleRate']}",
        "WinRate:0", # TODO We need to find this byte
        "WinLen:0", # TODO We need to find this byte
        # Use :X to format as Uppercase Hex (e.g., 10 -> A)
        f"Config0:{meta['Config0']:X}",
        f"Config1:{meta['Config1']:X}",
        f"Config2:{meta['Config2']:X}",
        f"Config3:{meta['Config3']:X}",
        f"Bitmask:{meta['Bitmask']:X}"
    ]
    
    try:
        with open(txt_path, 'w') as f:
            f.write("\n".join(lines))
    except Exception as e:
        logger.error(f"Failed to write metadata txt: {e}")