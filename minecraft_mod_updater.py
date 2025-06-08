#!/usr/bin/env python3
"""
Minecraft Mod Updater

This script automatically updates installed Minecraft mods to their latest versions.
It uses the Modrinth platform for all mods.
"""

import os
import json
import shutil
import time
import zipfile
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse

# Constants
MODRINTH_API_BASE = "https://api.modrinth.com/v2"

# Default headers for API requests
HEADERS = {
    "User-Agent": "MinecraftModUpdater/1.0",
    "Accept": "application/json"
}

class ModUpdater:
    def __init__(self, mods_dir=None, backup_dir=None, minecraft_version=None, loader=None):
        """Initialize the mod updater with directories and Minecraft version."""
        self.mods_dir = self._get_default_mods_dir() if mods_dir is None else Path(mods_dir)
        self.backup_dir = Path(self.mods_dir, "../mod_backups") if backup_dir is None else Path(backup_dir)
        self.minecraft_version = minecraft_version
        self.loader = loader
        self.mods_data = {}
        self.update_count = 0
        self.check_count = 0
        self.not_found_count = 0
        
        # Create backup directory if it doesn't exist
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Timestamp for backups
        self.timestamp = time.strftime("%Y%m%d_%H%M%S")
        
    def _get_default_mods_dir(self):
        """Get the default mods directory based on the operating system."""
        home = Path.home()
        
        if os.name == 'nt':  # Windows
            return Path(os.getenv('APPDATA', str(home)), ".minecraft", "mods")
        elif os.name == 'posix':  # macOS/Linux
            if os.path.exists(Path(home, "Library", "Application Support", "minecraft")):  # macOS
                return Path(home, "Library", "Application Support", "minecraft", "mods")
            else:  # Linux
                return Path(home, ".minecraft", "mods")
        
        # Fallback
        return Path(home, ".minecraft", "mods")
        
    def scan_mods(self):
        """Scan the mods directory and identify all installed mods."""
        print(f"Scanning mods directory: {self.mods_dir}")
        
        if not self.mods_dir.exists():
            print(f"Error: Mods directory {self.mods_dir} does not exist.")
            return False
            
        mod_files = list(self.mods_dir.glob("*.jar"))
        
        if not mod_files:
            print("No mod files found.")
            return False
            
        print(f"Found {len(mod_files)} mod files.")
        
        # Process each mod file to extract information
        with ThreadPoolExecutor() as executor:
            executor.map(self.process_mod_file, mod_files)
            
        print(f"Successfully processed {len(self.mods_data)} mods.")
        return True
        
    def process_mod_file(self, mod_path):
        """Extract metadata from a mod file."""
        try:
            mod_id = None
            mod_name = None
            mod_loader = None
            
            # Try to extract the fabric.mod.json or META-INF/mods.toml
            with zipfile.ZipFile(mod_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                
                # Check for Fabric mod
                if 'fabric.mod.json' in file_list:
                    with zip_ref.open('fabric.mod.json') as f:
                        data = json.load(f)
                        mod_id = data.get('id')
                        mod_name = data.get('name')
                        mod_loader = 'fabric'
                
                # Check for Forge mod
                elif 'META-INF/mods.toml' in file_list:
                    with zip_ref.open('META-INF/mods.toml') as f:
                        content = f.read().decode('utf-8')
                        # Basic parsing of TOML
                        for line in content.split('\n'):
                            if line.startswith('modId'):
                                mod_id = line.split('=')[1].strip().strip('"\'')
                            elif line.startswith('displayName'):
                                mod_name = line.split('=')[1].strip().strip('"\'')
                            if mod_id and mod_name:
                                break
                        mod_loader = 'forge'
                
                # Check for mcmod.info (older Forge)
                elif 'mcmod.info' in file_list:
                    with zip_ref.open('mcmod.info') as f:
                        data = json.load(f)
                        if isinstance(data, list) and data:
                            mod_id = data[0].get('modid')
                            mod_name = data[0].get('name')
                        elif isinstance(data, dict) and 'modList' in data:
                            mod_id = data['modList'][0].get('modid')
                            mod_name = data['modList'][0].get('name')
                        mod_loader = 'forge'
            
            # If we found a mod ID
            if mod_id and (self.loader is None or self.loader == mod_loader):
                self.mods_data[mod_path.name] = {
                    'path': str(mod_path),
                    'mod_id': mod_id,
                    'mod_name': mod_name or mod_id,  # Use ID as fallback if name not found
                    'current_file': mod_path.name,
                    'loader': mod_loader
                }
                print(f"Found mod: {mod_id} ({mod_path.name})")
            else:
                print(f"Warning: Could not identify mod ID for {mod_path.name}")
                
        except Exception as e:
            print(f"Error processing mod file {mod_path.name}: {e}")
    
    def update_mods(self):
        """Update all mods to their latest versions using Modrinth."""
        if not self.mods_data:
            print("No mods data available. Run scan_mods() first.")
            return
            
        print(f"Checking {len(self.mods_data)} mods for updates on Modrinth...")
        
        # Process each mod
        for mod_name, mod_info in self.mods_data.items():
            try:
                self.check_count += 1
                self.update_modrinth_mod(mod_info)
            except Exception as e:
                print(f"Error updating {mod_name}: {e}")
                
        print(f"Update complete. Checked {self.check_count} mods.")
        print(f"Updated {self.update_count} mods.")
        print(f"Could not find {self.not_found_count} mods on Modrinth.")
        
    def backup_mods(self):
        """Create a backup of all mods."""
        backup_folder = Path(self.backup_dir, f"backup_{self.timestamp}")
        backup_folder.mkdir(parents=True, exist_ok=True)
        
        print(f"Creating backup in {backup_folder}")
        
        for mod_name, mod_info in self.mods_data.items():
            try:
                src_path = Path(mod_info['path'])
                dst_path = Path(backup_folder, src_path.name)
                shutil.copy2(src_path, dst_path)
            except Exception as e:
                print(f"Error backing up {mod_name}: {e}")
                
        print(f"Backup complete. {len(self.mods_data)} mods backed up.")
        
    def update_modrinth_mod(self, mod_info):
        """Update a mod from Modrinth."""
        mod_id = mod_info['mod_id']
        mod_name = mod_info['mod_name']
        current_file = mod_info['current_file']
        
        print(f"Checking for updates for mod: {mod_name} ({mod_id})")
        
        # First try direct lookup by mod_id
        try:
            # Try to find the project directly by its ID
            response = requests.get(f"{MODRINTH_API_BASE}/project/{mod_id}", headers=HEADERS)
            
            # If we get a 404, try to search for the project instead
            if response.status_code == 404:
                print(f"Project {mod_id} not found directly, trying search...")
                return self._search_and_update_mod(mod_info)
                
            response.raise_for_status()  # Handle other errors
            project = response.json()
            project_id = project['id']
            
            # Get latest version compatible with the specified Minecraft version
            version_url = f"{MODRINTH_API_BASE}/project/{project_id}/version"
            if self.minecraft_version:
                version_url += f"?game_versions=[\"{self.minecraft_version}\"]"
                
            response = requests.get(version_url, headers=HEADERS)
            response.raise_for_status()
            versions = response.json()
            
            if not versions:
                print(f"No compatible versions found for {mod_name}")
                return
                
            # Get the latest version
            latest_version = versions[0]
            
            # Download the latest version
            download_url = latest_version['files'][0]['url']
            new_filename = latest_version['files'][0]['filename']
            
            # Skip if already up to date
            if new_filename == current_file:
                print(f"Mod {mod_name} is already up to date")
                return
                
            # Download and update the mod
            self._download_and_replace_mod(mod_info['path'], download_url, new_filename)
            self.update_count += 1
            
            print(f"Updated {mod_name} from {current_file} to {new_filename}")
            
        except requests.exceptions.RequestException as e:
            if "404" in str(e):
                self._search_and_update_mod(mod_info)
            else:
                print(f"Error fetching data from Modrinth for {mod_name}: {e}")
        except Exception as e:
            print(f"Error updating mod {mod_name}: {e}")
    
    def _search_and_update_mod(self, mod_info):
        """Search for a mod on Modrinth and update it if found."""
        mod_id = mod_info['mod_id']
        mod_name = mod_info['mod_name']
        current_file = mod_info['current_file']
        
        try:
            # Search for the mod using both ID and name
            search_terms = [mod_id]
            if mod_name and mod_name != mod_id:
                search_terms.append(mod_name)
                
            # Try each search term
            project = None
            for term in search_terms:
                search_url = f"{MODRINTH_API_BASE}/search"
                params = {
                    'query': term,
                    'limit': 5,
                    'facets': '[[\"project_type:mod\"]]'  # Only search for mods
                }
                
                response = requests.get(search_url, headers=HEADERS, params=params)
                response.raise_for_status()
                search_results = response.json()
                
                # Check if we have results
                if search_results['hits']:
                    # Find the best match
                    best_match = None
                    best_score = 0
                    
                    for hit in search_results['hits']:
                        # Calculate match score (simple algorithm)
                        score = 0
                        if hit['slug'] == mod_id.lower():
                            score += 10
                        if hit['title'].lower() == mod_name.lower():
                            score += 10
                        if mod_id.lower() in hit['slug']:
                            score += 5
                        if mod_name.lower() in hit['title'].lower():
                            score += 5
                            
                        if score > best_score:
                            best_score = score
                            best_match = hit
                    
                    # If we found a decent match
                    if best_match and best_score >= 5:
                        project = best_match
                        break
            
            # If we found a project
            if project:
                project_id = project['project_id']
                
                # Get latest version compatible with the specified Minecraft version
                version_url = f"{MODRINTH_API_BASE}/project/{project_id}/version"
                if self.minecraft_version:
                    version_url += f"?game_versions=[\"{self.minecraft_version}\"]"
                    
                response = requests.get(version_url, headers=HEADERS)
                response.raise_for_status()
                versions = response.json()
                
                if not versions:
                    print(f"No compatible versions found for {mod_name}")
                    return
                    
                # Get the latest version
                latest_version = versions[0]
                
                # Download the latest version
                download_url = latest_version['files'][0]['url']
                new_filename = latest_version['files'][0]['filename']
                
                # Skip if already up to date
                if new_filename == current_file:
                    print(f"Mod {mod_name} is already up to date")
                    return
                    
                # Download and update the mod
                self._download_and_replace_mod(mod_info['path'], download_url, new_filename)
                self.update_count += 1
                
                print(f"Updated {mod_name} from {current_file} to {new_filename}")
            else:
                print(f"Could not find {mod_name} on Modrinth")
                self.not_found_count += 1
                
        except requests.exceptions.RequestException as e:
            print(f"Error searching for {mod_name} on Modrinth: {e}")
        except Exception as e:
            print(f"Error updating mod {mod_name}: {e}")
    
    def _download_and_replace_mod(self, old_path, download_url, new_filename):
        """Download a new mod version and replace the old one."""
        try:
            # Download the new version
            response = requests.get(download_url, headers=HEADERS)
            response.raise_for_status()
            
            # Path for the new file
            new_path = Path(self.mods_dir, new_filename)
            
            # Write the new file
            with open(new_path, 'wb') as f:
                f.write(response.content)
                
            # Remove the old file if it's different from the new one
            if old_path != str(new_path):
                os.remove(old_path)
                
            return True
        except Exception as e:
            print(f"Error downloading mod: {e}")
            return False

def main():
    """Main function to run the mod updater."""
    parser = argparse.ArgumentParser(description='Minecraft Mod Updater (Modrinth Only)')
    parser.add_argument('--mods-dir', type=str, help='Path to the mods directory')
    parser.add_argument('--backup-dir', type=str, help='Path to the backup directory')
    parser.add_argument('--minecraft-version', type=str, help='Minecraft version (e.g., 1.20.1)')
    parser.add_argument('--loader', type=str, choices=['fabric', 'forge'], help='Mod loader type (fabric/forge)')
    parser.add_argument('--no-backup', action='store_true', help='Skip creating backups')
    
    args = parser.parse_args()
    
    # Initialize updater
    updater = ModUpdater(
        mods_dir=args.mods_dir,
        backup_dir=args.backup_dir,
        minecraft_version=args.minecraft_version,
        loader=args.loader
    )
    
    print("Minecraft Mod Updater (Modrinth Only)")
    print("-" * 40)
    print(f"Mods directory: {updater.mods_dir}")
    if args.no_backup:
        print("Backups: Disabled")
    else:
        print(f"Backup directory: {updater.backup_dir}")
    if args.minecraft_version:
        print(f"Minecraft version: {args.minecraft_version}")
    if args.loader:
        print(f"Loader: {args.loader}")
    print("-" * 40)
    
    # Run the update process
    if updater.scan_mods():
        if not args.no_backup:
            updater.backup_mods()
        updater.update_mods()
    else:
        print("Failed to scan mods. Update aborted.")

if __name__ == "__main__":
    main()