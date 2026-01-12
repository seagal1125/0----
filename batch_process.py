import os
import subprocess
import time

def run_command(command):
    print(f"Executing: {command}")
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return False

def main():
    start_vol = 154
    end_vol = 147
    
    # Process from newest to oldest
    volumes = range(start_vol, end_vol - 1, -1)
    
    success_count = 0
    fail_count = 0
    
    failed_volumes = []

    for vol in volumes:
        print(f"\n{'='*30}")
        print(f"Processing Volume {vol}")
        print(f"{'='*30}")
        
        # 1. Identify Input File
        input_file = f"{vol}.txt"
        if not os.path.exists(input_file):
            input_file = f"raw_{vol}.txt"
            if not os.path.exists(input_file):
                print(f"Skipping Volume {vol}: No input file found ({vol}.txt or raw_{vol}.txt)")
                fail_count += 1
                failed_volumes.append(vol)
                continue
        
        print(f"Found input file: {input_file}")
        
        # 2. Parse Raw Text to Markdown
        cmd_parse = f"python3 parse_raw.py {input_file} --volume {vol}"
        if not run_command(cmd_parse):
            print(f"Failed to parse Volume {vol}")
            fail_count += 1
            failed_volumes.append(vol)
            continue
            
        # 3. Fetch IDs and Generate HTML
        md_file = f"YouTube_Playlist_{vol}.md"
        html_file = f"index_{vol}.html"
        title = f"最新排行{vol}"
        
        cmd_fetch = f"python3 fetch_ids.py {md_file} --output {html_file} --title \"{title}\""
        if not run_command(cmd_fetch):
            print(f"Failed to fetch IDs for Volume {vol}")
            fail_count += 1
            failed_volumes.append(vol)
            continue
            
        success_count += 1
        print(f"Volume {vol} processed successfully!")
        
        # Optional: Sleep briefly to avoid hitting potential rate limits too hard (though yt-dlp usually handles this)
        time.sleep(2)

    print(f"\n{'='*30}")
    print("Batch Processing Complete")
    print(f"{'='*30}")
    print(f"Successful: {success_count}")
    print(f"Failed: {fail_count}")
    
    if failed_volumes:
        print(f"Failed Volumes: {failed_volumes}")

    # 4. Update Master Index
    print("\nUpdating Master Index...")
    if run_command("python3 generate_master_index.py"):
        print("Master Index updated successfully.")
    else:
        print("Failed to update Master Index.")

if __name__ == "__main__":
    main()
