# Free Fire Game Bot - Helper Functions Module
# De-obfuscated version for maintainability

import requests
import os
import psutil
import sys
import jwt
import pickle
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
from protobuf_decoder.protobuf_decoder import Parser
from crypto import (
    encrypt_aes, decode_packet, encode_uid, format_message
)
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# ==================== TOKEN MANAGEMENT ====================

TOKEN_FETCH_URL = 'https://tokens-asfufvfshnfkhvbb.francecentral-01.azurewebsites.net/ReQuesT?&type=ToKens'
TOKEN_FILE = "token.txt"


def fetch_tokens():
    """Continuously fetch and update authentication tokens from server"""
    while True:
        try:
            response = requests.get(TOKEN_FETCH_URL)
            response_text = response.text
            start_idx = response_text.find("ToKens : [")
            
            if start_idx != -1:
                end_idx = response_text.find("]", start_idx)
                token_list = [x.strip(" '\"") for x in response_text[start_idx+11:end_idx].split(',') if x.strip()]
                
                if token_list:
                    with open(TOKEN_FILE, "w") as f:
                        f.write(random.choice(token_list))
        except Exception as e:
            pass
        
        # Refresh tokens every 5 hours
        time.sleep(5 * 60 * 60)


# Start token fetch in background daemon thread
Thread(target=fetch_tokens, daemon=True).start()


def get_token():
    """Read current token from file"""
    try:
        with open(TOKEN_FILE) as f:
            return f.read().strip()
    except FileNotFoundError:
        print("Warning: Token file not found")
        return None


# ==================== EMOTE FUNCTIONS ====================

def send_emote_request(jwt_token, url):
    """Send emote choice request to Free Fire server"""
    endpoint = f"{url}/ChooseEmote"
    
    headers = {
        "Accept-Encoding": "gzip",
        "Authorization": f"Bearer {jwt_token}",
        "Connection": "Keep-Alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Expect": "100-continue",
        "ReleaseVersion": "OB51",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)",
        "X-GA": "v1 1",
        "X-Unity-Version": "2018.4.11f1",
    }
    
    # Emote selection packet data
    emote_data = bytes.fromhex("CA F6 83 22 2A 25 C7 BE FE B5 1F 59 54 4D B3 13")
    
    try:
        requests.post(endpoint, headers=headers, data=emote_data)
    except Exception as e:
        print(f"Error sending emote request: {e}")


# ==================== PLAYER STATISTICS ====================

async def get_player_likes(player_id):
    """Fetch player's likes and related statistics"""
    try:
        url = f'https://tokens-asfufvfshnfkhvbb.francecentral-01.azurewebsites.net/ReQuesT?id={player_id}&type=likes'
        response = requests.get(url)
        response_text = response.text
        
        # Parse response using regex patterns
        find_pattern = lambda pattern: re.search(pattern, response_text)
        
        patterns = {
            'name': r"PLayer NamE\s*:\s*(.+)",
            'level': r"PLayer SerVer\s*:\s*(.+)",
            'exp': r"Exp\s*:\s*(\d+)",
            'likes_before': r"LiKes BeFore\s*:\s*(\d+)",
            'likes_after': r"LiKes After\s*:\s*(\d+)",
            'likes_given': r"LiKes GiVen\s*:\s*(\d+)"
        }
        
        results = {}
        for key, pattern in patterns.items():
            match = find_pattern(pattern)
            if key == 'level':
                results[key] = f"{match.group(1)}" if match else None
            elif key in ['likes_before', 'likes_after', 'likes_given']:
                results[key] = int(match.group(1)) if match else None
            else:
                results[key] = match.group(1) if match else None
        
        return results
        
    except Exception as e:
        print(f"Error fetching player likes: {e}")
        return {}


async def request_spam(player_id):
    """Request spam action for player"""
    try:
        url = f'https://tokens-asfufvfshnfkhvbb.francecentral-01.azurewebsites.net/ReQuesT?id={player_id}&type=spam'
        response = requests.get(url)
        
        success_message = '[SuccessFuLy] -> SenDinG Spam ReQuesTs !'
        return response.status_code in [200, 201] and success_message in response.text
    except Exception as e:
        print(f"Error requesting spam: {e}")
        return False


# ==================== PLAYER INFO FUNCTIONS ====================

async def get_player_name(uid, token=None):
    """Fetch player's in-game name"""
    try:
        if token is None:
            token = get_token()
        
        hex_data = f"08{await encode_uid(uid, type_flag='Uid')}1007"
        encrypted_data = await encrypt_aes(hex_data)
        data = bytes.fromhex(encrypted_data)
        
        url = "https://clientbp.common.ggbluefox.com/GetPlayerPersonalShow"
        headers = {
            'X-Unity-Version': '2018.4.11f1',
            'ReleaseVersion': 'OB51',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-GA': 'v1 1',
            'Authorization': f'Bearer {token}',
            'Content-Length': '16',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
            'Host': 'clientbp.ggblueshark.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }
        
        response = requests.post(url, headers=headers, data=data, verify=False)
        
        if response.status_code in [200, 201]:
            packet_hex = binascii.hexlify(response.content).decode('utf-8')
            packet_data = json.loads(await decode_packet(packet_hex))
            
            try:
                player_name = packet_data["1"]["data"]["3"]["data"]
                return player_name
            except KeyError:
                return ''
        
        return ''
        
    except Exception as e:
        print(f"Error getting player name: {e}")
        return ''


async def get_player_info(uid, token=None):
    """Fetch comprehensive player information including clan details"""
    try:
        if token is None:
            token = get_token()
        
        hex_data = f"08{await encode_uid(uid, type_flag='Uid')}1007"
        encrypted_data = await encrypt_aes(hex_data)
        data = bytes.fromhex(encrypted_data)
        
        url = "https://clientbp.common.ggbluefox.com/GetPlayerPersonalShow"
        headers = {
            'X-Unity-Version': '2018.4.11f1',
            'ReleaseVersion': 'OB51',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-GA': 'v1 1',
            'Authorization': f'Bearer {token}',
            'Content-Length': '16',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
            'Host': 'clientbp.ggblueshark.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }
        
        response = requests.post(url, headers=headers, data=data, verify=False)
        
        if response.status_code in [200, 201]:
            packet_hex = binascii.hexlify(response.content).decode('utf-8')
            packet_data = json.loads(await decode_packet(packet_hex))
            
            try:
                # Extract player info
                player_uid = str(packet_data["1"]["data"]["1"]["data"])
                player_likes = packet_data["1"]["data"]["21"]["data"]
                player_name = packet_data["1"]["data"]["3"]["data"]
                player_server = packet_data["1"]["data"]["5"]["data"]
                player_bio = packet_data["9"]["data"]["9"]["data"]
                player_level = packet_data["1"]["data"]["6"]["data"]
                account_created = datetime.fromtimestamp(
                    packet_data["1"]["data"]["44"]["data"]
                ).strftime("%I:%M %p - %d/%m/%y")
                last_login = datetime.fromtimestamp(
                    packet_data["1"]["data"]["24"]["data"]
                ).strftime("%I:%M %p - %d/%m/%y")
                
                # Try to extract clan info
                has_clan = True
                try:
                    clan_id = packet_data["6"]["data"]["1"]["data"]
                    clan_name = packet_data["6"]["data"]["2"]["data"]
                    clan_leader = packet_data["6"]["data"]["3"]["data"]
                    clan_level = packet_data["6"]["data"]["4"]["data"]
                    clan_members = packet_data["6"]["data"]["6"]["data"]
                    clan_leader_name = packet_data["7"]["data"]["3"]["data"]
                except KeyError:
                    has_clan = False
                
                # Format output
                output = f'''
[b][c][90EE90] [Successfully] - Get Player Info!

[FFFF00][1] - Profile Info:
[ffffff]	
 Name : {player_name}
 UID : {format_message(player_uid)}
 Likes : {format_message(player_likes)}
 Level : {player_level}
 Server : {player_server}
 Bio : {player_bio}
 Created : {account_created}
 Last Login : {last_login}
'''
                
                if has_clan:
                    output += f'''
[b][c][FFFF00][2] - Guild Info:
[ffffff]
 Guild Name : {clan_name}
 Guild UID : {format_message(clan_id)}
 Guild Level : {clan_level}
 Guild Members : {clan_members}
 Leader UID : {format_message(clan_leader)}
 Leader Name : {clan_leader_name}
'''
                
                output += "\n  [90EE90]Dev: C4 Team Official\n"
                return output.replace('[i]', '')
                
            except Exception as e:
                print(f"Error parsing player info: {e}")
                return '\n[b][c][FFD700]Failed getting player info!\n'
        else:
            return '\n[b][c][FFD700]Failed getting player info!\n'
        
    except Exception as e:
        print(f"Error fetching player info: {e}")
        return '\n[b][c][FFD700]Failed getting player info!\n'


# ==================== FRIEND MANAGEMENT ====================

async def delete_friend(friend_id, token):
    """Remove player from friends list"""
    try:
        print(f'Deleting friend: {friend_id}')
        
        url = 'https://clientbp.common.ggbluefox.com/RemoveFriend'
        headers = {
            'X-Unity-Version': '2018.4.11f1',
            'ReleaseVersion': 'OB51',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-GA': 'v1 1',
            'Authorization': f'Bearer {token}',
            'Content-Length': '16',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
            'Host': 'clientbp.ggblueshark.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }
        
        hex_data = f"08a7c4839f1e10{await encode_uid(friend_id, type_flag='Uid')}"
        encrypted_data = await encrypt_aes(hex_data)
        data = bytes.fromhex(encrypted_data)
        
        response = requests.post(url, headers=headers, data=data, verify=False)
        
        if response.status_code == 400 and 'BR_FRIEND_NOT_SAME_REGION' in response.text:
            return f'[b][c]ID: {format_message(friend_id)} not in same region!'
        elif response.status_code == 200:
            return f'[b][c]Successfully deleted ID: {format_message(friend_id)}!'
        else:
            return f'[b][c]Error deleting friend!'
            
    except Exception as e:
        print(f"Error deleting friend: {e}")
        return f'[b][c]Error deleting friend: {e}!'


# ==================== UID VALIDATION ====================

async def check_uid_status(uid):
    """Check if UID is in database with expiration status"""
    try:
        response = requests.get("https://panel-g2ccathtf6gdcmdw.polandcentral-01.azurewebsites.net/Uids")
        
        if response.status_code not in [200, 201]:
            return False
        
        lines = response.text.splitlines()
        
        for i, line in enumerate(lines):
            if f' - Uid : {uid}' in line:
                expire = None
                status = None
                
                # Look for expiration and status in following lines
                for sub_line in lines[i:]:
                    if "Expire In" in sub_line:
                        expire_match = re.search(r"Expire In\s*:\s*(.*)", sub_line)
                        if expire_match:
                            expire = expire_match.group(1).strip()
                    
                    if "Status" in sub_line:
                        status_match = re.search(r"Status\s*:\s*(\w+)", sub_line)
                        if status_match:
                            status = status_match.group(1)
                    
                    if expire and status:
                        return status, expire
                
                return False
        
        return False
        
    except Exception as e:
        print(f"Error checking UID status: {e}")
        return False
