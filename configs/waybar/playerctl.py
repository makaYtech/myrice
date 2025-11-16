#!/usr/bin/env python3
"""
Waybar playerctl module script
Outputs JSON format for Waybar custom module
"""

import subprocess
import json

def get_player_icon(player_name):
    """Get nerd font icon for player"""
    player_name = player_name.lower()
    if 'spotify' in player_name:
        return ''

def run_playerctl_command(args):
    """Run playerctl command and return output"""
    try:
        result = subprocess.run(
            ['playerctl'] + args,
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip(), result.returncode
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return "", 1

def get_available_players():
    """Get list of available players"""
    output, returncode = run_playerctl_command(['-l'])
    if returncode == 0 and output:
        return [line.strip() for line in output.split('\n') if line.strip()]
    return []

def get_player_status(player_name=None):
    """Get current player status"""
    args = ['status']
    if player_name:
        args = ['-p', player_name] + args

    output, returncode = run_playerctl_command(args)
    if returncode == 0:
        return output.capitalize()
    return 'Stopped'

def get_metadata(key=None, player_name=None):
    """Get metadata from playerctl"""
    args = ['metadata']
    if player_name:
        args = ['-p', player_name] + args
    if key:
        args.append(key)

    output, returncode = run_playerctl_command(args)
    if returncode == 0:
        return output
    return ""

def find_spotify_player(players):
    """Find Spotify player among available players"""
    for player in players:
        if 'spotify' in player.lower():
            return player
    return None

def main():
    """Main function"""
    players = get_available_players()
    
    # Ищем только Spotify плеер
    spotify_player = find_spotify_player(players)
    
    # Если Spotify не найден, выводим пустой результат
    if not spotify_player:
        result = {
            "text": "",
            "tooltip": "",
            "class": "inactive"
        }
        print(json.dumps(result))
        return

    # Получаем статус Spotify
    status = get_player_status(spotify_player)

    # Получаем метаданные Spotify
    title = get_metadata("xesam:title", spotify_player)
    artist = get_metadata("xesam:artist", spotify_player)
    album = get_metadata("xesam:album", spotify_player)

    # Форматируем отображаемый текст
    if title and artist:
        display_text = f" {title} - {artist}"
    elif title:
        display_text = f" {title}"
    else:
        display_text = " No media"

    # Форматируем всплывающую подсказку
    tooltip_lines = []
    if title and artist:
        tooltip_lines.append(f"{artist} - {title}")
    elif title:
        tooltip_lines.append(title)

    if album:
        tooltip_lines.append(f"Album: {album}")

    tooltip_lines.append("Player: Spotify")
    tooltip = "\n".join(tooltip_lines)

    # Определяем класс для стилизации
    class_name = status.lower() if status in ['Playing', 'Paused'] else 'stopped'

    # Создаем результат
    result = {
        "text": display_text,
        "tooltip": tooltip,
        "class": class_name
    }

    print(json.dumps(result))

if __name__ == "__main__":
    main()