# Free Fire Game Bot - Cryptography Module
# De-obfuscated version for maintainability and security audit

import requests
import json
import binascii
import time
import urllib3
import base64
import datetime
import re
import socket
import threading
import random
import os
import asyncio
from protobuf_decoder.protobuf_decoder import Parser
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Hardcoded encryption keys - should be moved to environment variables for security
ENCRYPTION_KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
ENCRYPTION_IV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])


# ==================== ENCRYPTION FUNCTIONS ====================

async def encrypt_aes(hex_data):
    """Encrypt data using AES-CBC with standard key and IV"""
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, ENCRYPTION_IV)
    return cipher.encrypt(pad(bytes.fromhex(hex_data), AES.block_size)).hex()


async def decrypt_aes(hex_data):
    """Decrypt data using AES-CBC with standard key and IV"""
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, ENCRYPTION_IV)
    return unpad(cipher.decrypt(bytes.fromhex(hex_data)), AES.block_size).hex()


async def encrypt_packet(hex_data, key, iv):
    """Encrypt packet with custom key and IV"""
    return AES.new(key, AES.MODE_CBC, iv).encrypt(pad(bytes.fromhex(hex_data), 16)).hex()


async def decrypt_packet(hex_data, key, iv):
    """Decrypt packet with custom key and IV"""
    return unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(bytes.fromhex(hex_data)), 16).hex()


# ==================== PROTOBUF ENCODING FUNCTIONS ====================

async def encode_uid(user_id, type_flag):
    """Encode user ID in protobuf variable-length format"""
    encoded = []
    user_id = int(user_id)
    while user_id:
        encoded.append((user_id & 0x7F) | (0x80 if user_id > 0x7F else 0))
        user_id >>= 7
    return bytes(encoded).hex() if type_flag == 'Uid' else None


async def encode_varint(number):
    """Encode number as protobuf varint"""
    if number < 0:
        return b''
    encoded = []
    while True:
        byte_value = number & 0x7F
        number >>= 7
        if number:
            byte_value |= 0x80
        encoded.append(byte_value)
        if not number:
            break
    return bytes(encoded)


def decode_uid(hex_data):
    """Decode user ID from protobuf variable-length format"""
    n = s = 0
    for b in bytes.fromhex(hex_data):
        n |= (b & 0x7F) << s
        if not b & 0x80:
            break
        s += 7
    return n


async def create_variant(field_number, value):
    """Create protobuf variant field"""
    field_header = (field_number << 3) | 0
    return await encode_varint(field_header) + await encode_varint(value)


async def create_length(field_number, value):
    """Create protobuf length-delimited field"""
    field_header = (field_number << 3) | 2
    encoded_value = value.encode() if isinstance(value, str) else value
    return await encode_varint(field_header) + await encode_varint(len(encoded_value)) + encoded_value


async def create_proto(fields):
    """Build complete protobuf packet from field dictionary"""
    packet = bytearray()
    for field, value in fields.items():
        if isinstance(value, dict):
            nested_packet = await create_proto(value)
            packet.extend(await create_length(field, nested_packet))
        elif isinstance(value, int):
            packet.extend(await create_variant(field, value))
        elif isinstance(value, str) or isinstance(value, bytes):
            packet.extend(await create_length(field, value))
    return packet


async def decode_hex(hex_value):
    """Convert hex value to padded hex string"""
    result = hex(hex_value)
    formatted = str(result)[2:]
    if len(formatted) == 1:
        formatted = "0" + formatted
    return formatted


async def fix_packet(parsed_results):
    """Convert parsed protobuf results to dictionary format"""
    result_dict = {}
    for result in parsed_results:
        field_data = {}
        field_data['wire_type'] = result.wire_type
        if result.wire_type == "varint":
            field_data['data'] = result.data
        if result.wire_type == "string":
            field_data['data'] = result.data
        if result.wire_type == "bytes":
            field_data['data'] = result.data
        elif result.wire_type == 'length_delimited':
            field_data["data"] = await fix_packet(result.data.results)
        result_dict[result.field] = field_data
    return result_dict


async def decode_packet(input_text):
    """Parse and decode protobuf packet"""
    try:
        parsed_results = Parser().parse(input_text)
        parsed_results_objects = parsed_results
        parsed_results_dict = await fix_packet(parsed_results_objects)
        json_data = json.dumps(parsed_results_dict)
        return json_data
    except Exception as e:
        print(f"Error decoding packet: {e}")
        return None


# ==================== PACKET GENERATION FUNCTIONS ====================

async def generate_packet(packet_hex, packet_type, key, iv):
    """Encapsulate and finalize packet with header and encryption"""
    encrypted_packet = await encrypt_packet(packet_hex, key, iv)
    length_hex = await decode_hex(int(len(encrypted_packet) // 2))
    
    if len(length_hex) == 2:
        header = packet_type + "000000"
    elif len(length_hex) == 3:
        header = packet_type + "00000"
    elif len(length_hex) == 4:
        header = packet_type + "0000"
    elif len(length_hex) == 5:
        header = packet_type + "000"
    else:
        print('Error: Unable to generate packet header')
        return None
    
    return bytes.fromhex(header + length_hex + encrypted_packet)


async def generate_login_packet(uid, code, key, iv):
    """Generate login/authentication packet"""
    fields = {
        1: 4,
        2: {
            1: uid,
            3: uid,
            8: 1,
            9: {
                2: 161,
                4: "y[WW",
                6: 11,
                8: "1.114.18",
                9: 3,
                10: 1
            },
            10: str(code),
        }
    }
    return await generate_packet((await create_proto(fields)).hex(), '0515', key, iv)


async def generate_rejection_message(squad_owner, uid, key, iv):
    """Generate squad rejection message packet"""
    random_banner = f"""
[000000]
[000000]
[000000]
[000000]
[000000]
[000000]
[000000]
[000000]
[000000]
[000000]
[000000]
[000000]
[000000]
[000000]
[000000]
[000000]
[000000]
[000000]
[000000]
[000000]
[000000]
[000000]
[000000]
[000000]
[000000]
[000000]
[000000]
[000000]
[FF0000]███████████████████████████
███████████████████████████
███████▀▀▀░░░░░░░▀▀▀███████
████▀░░░░░░░░░░░░░░░░░▀████
███│░░░░░░░░░░░░░░░░░░░│███
██▌│░░░░░░░░░░░░░░░░░░░│▐██
██░└┐░░░░░░░░░░░░░░░░░┌┘░██
██░░└┐░░░░░░░░░░░░░░░┌┘░░██
██░░┌┘▄▄▄▄▄░░░░░▄▄▄▄▄└┐░░██
██▌░│██████▌░░░▐██████│░▐██
███░│▐███▀▀░░▄░░▀▀███▌│░███
██▀─┘░░░░░░░▐█▌░░░░░░░└─▀██
██▄░░░▄▄▄▓░░▀█▀░░▓▄▄▄░░░▄██
████▄─┘██▌░░░░░░░▐██└─▄████
█████░░▐█─┬┬┬┬┬┬┬─█▌░░█████
████▌░░░▀┬┼┼┼┼┼┼┼┬▀░░░▐████
█████▄░░░└┴┴┴┴┴┴┴┘░░░▄█████
███████▄░░░░░░░░░░░▄███████
██████████▄▄▄▄▄▄▄██████████
███████████████████████████
[000000]
[1E90FF]                    Ｄ　Ｅ　Ｖ　Ｅ　Ｌ　Ｏ　Ｐ　Ｅ　Ｒ　 : [FF0000] D A J A L  F F
[000000]
[9400D3]                  Ｍ　Ａ　Ｄ　Ｅ　　Ｂ　Ｙ　 : [FF0000] D A J A L  F F
[000000]
[FFD700]                    Ｙ　Ｏ　Ｕ　Ｔ　Ｕ　Ｂ　Ｅ　 : [FF0000] D　A　J　A　L 　F　F
[FFD700]                  Ｉ　Ｎ　Ｓ　Ｔ　Ａ　Ｇ　Ｒ　Ａ　Ｍ　 : [FF0000] @ISMAIL_ff
[FFD700]                Ｊ　Ｏ　Ｉ　Ｎ　　Ｔ　Ｅ　Ｌ　Ｅ　Ｇ　Ｒ　Ａ　Ｍ　 : [FF0000] @ISMAIL
[000000]
[FF0000]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[FF0000]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[000000]
[000000]
[000000]
[000000]
[000000]
"""
    fields = {
        1: 5,
        2: {
            1: int(squad_owner),
            2: 1,
            3: int(uid),
            4: random_banner
        }
    }
    return await generate_packet((await create_proto(fields)).hex(), '0515', key, iv)


# ==================== PACKET-SPECIFIC FUNCTIONS ====================

async def lag_squad(key, iv):
    """Generate lag squad packet"""
    fields = {
        1: 15,
        2: {
            1: 1124759936,
            2: 1
        }
    }
    return await generate_packet((await create_proto(fields)).hex(), '0515', key, iv)


async def get_status(player_uid, key, iv):
    """Get player status packet"""
    player_uid = await encode_uid(player_uid, type_flag='Uid')
    if len(player_uid) == 8:
        packet = f'080112080a04{player_uid}1005'
    elif len(player_uid) == 10:
        packet = f"080112090a05{player_uid}1005"
    return await generate_packet(packet, '0f15', key, iv)


async def spam_room(uid, room_id, message, key, iv):
    """Generate room spam packet"""
    fields = {
        1: 78,
        2: {
            1: int(room_id),
            2: f"[{await get_random_color()}]{message}",
            3: {2: 1, 3: 1},
            4: 330,
            5: 1,
            6: 201,
            10: await get_random_banner(),
            11: int(uid),
            12: 1
        }
    }
    return await generate_packet((await create_proto(fields)).hex(), '0e15', key, iv)


async def generate_join_squads_packet(code, key, iv):
    """Generate squad join packet"""
    fields = {
        1: 4,
        2: {
            4: bytes.fromhex("01090a0b121920"),
            5: str(code),
            6: 6,
            8: 1,
            9: {
                2: 800,
                6: 11,
                8: "1.111.1",
                9: 5,
                10: 1
            }
        }
    }
    return await generate_packet((await create_proto(fields)).hex(), '0515', key, iv)


async def generate_join_global(owner, code, key, iv):
    """Generate global join packet"""
    fields = {
        1: 4,
        2: {
            1: owner,
            6: 1,
            8: 1,
            13: "en",
            15: code,
            16: "OR",
        }
    }
    return await generate_packet((await create_proto(fields)).hex(), '0515', key, iv)


async def function_fs(key, iv):
    """Unknown function (FS abbreviation)"""
    fields = {
        1: 9,
        2: {
            1: 13256361202
        }
    }
    return await generate_packet((await create_proto(fields)).hex(), '0515', key, iv)


async def send_emote(target, emote_id, key, iv, region):
    """Send emote packet to target player"""
    fields = {
        1: 21,
        2: {
            1: 804266360,
            2: 909000001,
            5: {
                1: target,
                3: emote_id,
            }
        }
    }
    
    if region.lower() == "ind":
        packet = '0514'
    elif region.lower() == "bd":
        packet = "0519"
    else:
        packet = "0515"
    
    return await generate_packet((await create_proto(fields)).hex(), packet, key, iv)


async def authenticate_clan(clan_uid, auth_code, key, iv):
    """Authenticate with clan"""
    fields = {1: 3, 2: {1: int(clan_uid), 2: 1, 4: str(auth_code)}}
    return await generate_packet((await create_proto(fields)).hex(), '1201', key, iv)


async def authenticate_global(key, iv):
    """Global authentication packet"""
    fields = {
        1: 3,
        2: {
            2: 5,
            3: "en"
        }
    }
    return await generate_packet((await create_proto(fields)).hex(), '1215', key, iv)


async def authenticate_chat(message_type, uid, code, key, iv):
    """Authenticate for chat"""
    fields = {
        1: message_type,
        2: {
            1: uid,
            3: "en",
            4: str(code)
        }
    }
    return await generate_packet((await create_proto(fields)).hex(), '1215', key, iv)


async def send_message(message, message_type, sub_type, room_id, key, iv):
    """Send general message"""
    fields = {
        1: room_id,
        2: message_type,
        3: sub_type,
        4: message,
        5: 1735129800,
        7: 2,
        9: {
            1: "xBesTo - C4",
            2: int(await get_random_banner()),
            3: 901048020,
            4: 330,
            5: 1001000001,
            8: "xBesTo - C4",
            10: 1,
            11: 1,
            13: {1: 2},
            14: {
                1: 12484827014,
                2: 8,
                3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
            }
        },
        10: "en",
        13: {3: 1}
    }
    packet = (await create_proto(fields)).hex()
    packet = "080112" + await encode_uid(len(packet) // 2, type_flag='Uid') + packet
    return await generate_packet(packet, '1201', key, iv)


async def send_squad_message(message, room_id, key, iv):
    """Send message in squad"""
    fields = {
        1: room_id,
        2: room_id,
        4: message,
        5: 1756580149,
        7: 2,
        8: 904990072,
        9: {
            1: "xBe4!sTo - C4",
            2: await get_random_banner(),
            4: 330,
            5: 1001000001,
            8: "xBe4!sTo - C4",
            10: 1,
            11: 1,
            13: {1: 2},
            14: {
                1: 1158053040,
                2: 8,
                3: "\u0010\u0015\b\n\u000b\u0015\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
            }
        },
        10: "en",
        13: {2: 2, 3: 1}
    }
    packet = (await create_proto(fields)).hex()
    packet = "080112" + await encode_uid(len(packet) // 2, type_flag='Uid') + packet
    return await generate_packet(packet, '1201', key, iv)


async def generate_ghost_packet(player_id, secret_code, key, iv):
    """Generate ghost mode packet"""
    fields = {
        1: 61,
        2: {
            1: int(player_id),
            2: {
                1: int(player_id),
                2: int(time.time()),
                3: "MR3SKR",
                5: 12,
                6: 9999999,
                7: 1,
                8: {
                    2: 1,
                    3: 1,
                },
                9: 3,
            },
            3: secret_code,
        },
    }
    return await generate_packet((await create_proto(fields)).hex(), '0515', key, iv)


async def open_squad(key, iv, region):
    """Open squad packet"""
    fields = {
        1: 1,
        2: {
            2: "\u0001",
            3: 1,
            4: 1,
            5: "en",
            9: 1,
            11: 1,
            13: 1,
            14: {
                2: 5756,
                6: 11,
                8: "1.111.5",
                9: 2,
                10: 4
            }
        }
    }
    
    if region.lower() == "ind":
        packet = '0514'
    elif region.lower() == "bd":
        packet = "0519"
    else:
        packet = "0515"
    
    return await generate_packet((await create_proto(fields)).hex(), packet, key, iv)


async def check_squad(number, uid, key, iv, region):
    """Check squad status"""
    fields = {
        1: 17,
        2: {
            1: int(uid),
            2: 1,
            3: int(number - 1),
            4: 62,
            5: "\u001a",
            8: 5,
            13: 329
        }
    }
    
    if region.lower() == "ind":
        packet = '0514'
    elif region.lower() == "bd":
        packet = "0519"
    else:
        packet = "0515"
    
    return await generate_packet((await create_proto(fields)).hex(), packet, key, iv)


async def send_invite(number, uid, key, iv, region):
    """Send squad invite"""
    fields = {
        1: 2,
        2: {
            1: int(uid),
            2: region,
            4: int(number)
        }
    }
    
    if region.lower() == "ind":
        packet = '0514'
    elif region.lower() == "bd":
        packet = "0519"
    else:
        packet = "0515"
    
    return await generate_packet((await create_proto(fields)).hex(), packet, key, iv)


async def exit_squad(exit_id, key, iv):
    """Exit squad packet"""
    fields = {
        1: 7,
        2: {
            1: exit_id,
        }
    }
    return await generate_packet((await create_proto(fields)).hex(), '0515', key, iv)


# ==================== HELPER FUNCTIONS ====================

def format_message(number):
    """Format message with separator"""
    return '🗿'.join(str(number)[i:i + 3] for i in range(0, len(str(number)), 3))


async def get_user_agent():
    """Get random user agent string"""
    versions = [
        '4.0.18P6', '4.0.19P7', '4.0.20P1', '4.1.0P3', '4.1.5P2', '4.2.1P8',
        '4.2.3P1', '5.0.1B2', '5.0.2P4', '5.1.0P1', '5.2.0B1', '5.2.5P3',
        '5.3.0B1', '5.3.2P2', '5.4.0P1', '5.4.3B2', '5.5.0P1', '5.5.2P3'
    ]
    models = [
        'SM-A125F', 'SM-A225F', 'SM-A325M', 'SM-A515F', 'SM-A725F', 'SM-M215F', 'SM-M325FV',
        'Redmi 9A', 'Redmi 9C', 'POCO M3', 'POCO M4 Pro', 'RMX2185', 'RMX3085',
        'moto g(9) play', 'CPH2239', 'V2027', 'OnePlus Nord', 'ASUS_Z01QD',
    ]
    android_versions = ['9', '10', '11', '12', '13', '14']
    languages = ['en-US', 'es-MX', 'pt-BR', 'id-ID', 'ru-RU', 'hi-IN']
    countries = ['USA', 'MEX', 'BRA', 'IDN', 'RUS', 'IND']
    
    version = random.choice(versions)
    model = random.choice(models)
    android = random.choice(android_versions)
    lang = random.choice(languages)
    country = random.choice(countries)
    
    return f"GarenaMSDK/{version}({model};Android {android};{lang};{country};)"


async def get_random_color():
    """Get random color code"""
    colors = [
        "32CD32", "00BFFF", "00FA9A", "90EE90", "FF4500", "FF6347", "FF69B4", "FF8C00",
        "FF6347", "FFD700", "FFDAB9", "F0F0F0", "F0E68C", "D3D3D3", "A9A9A9", "D2691E",
        "CD853F", "BC8F8F", "6A5ACD", "483D8B", "4682B4", "9370DB", "C71585", "FF8C00", "FFA07A"
    ]
    return random.choice(colors)


async def get_random_banner():
    """Get random banner/avatar ID"""
    banner_ids = [
        902000154, 902047010, 902000306, 902000160, 902048020, 902048021, 902000305, 902000003,
        902000016, 902000017, 902000019, 902031010, 902043025, 902043024, 902000020, 902000021,
        902000023, 902000070, 902000087, 902000108, 902000011, 902049020, 902049018, 902049017,
        902049016, 902049015, 902049003, 902033016, 902033017, 902033018, 902048018, 902000306,
        902000305, 902000079, 902051034
    ]
    return random.choice(banner_ids)


def _safe_get(d, *keys, default=None):
    """Safely get nested dictionary values"""
    for k in keys:
        if not isinstance(d, dict) or k not in d:
            return default
        d = d[k]
    return d


async def get_squad_data(packet_data):
    """Extract squad data from packet"""
    inner = _safe_get(packet_data, "5", "data", default={})
    uid = _safe_get(inner, "1", "data")
    chat_code = _safe_get(inner, "14", "data")
    squad_code = _safe_get(inner, "31", "data")
    
    if uid is None:
        raise ValueError(f"Missing required uid field in packet")
    
    return uid, chat_code, squad_code


async def send_room_chat_enhanced(message, room_id, key, iv, region):
    """Send enhanced room chat message with packet structure"""
    fields = {
        1: 1,
        2: {
            1: 9280892890,
            2: int(room_id),
            3: 3,
            4: f"[{await get_random_color()}]{message}",
            5: int(datetime.now().timestamp()),
            7: 2,
            9: {
                1: "ISMAIL FF!ㅤ",
                2: int(await get_random_banner()),
                4: 228,
                7: 1,
            },
            10: "en",
            13: {2: 1, 3: 1},
        },
    }
    
    packet = (await create_proto(fields)).hex()
    return await generate_packet(packet, '1215', key, iv)
