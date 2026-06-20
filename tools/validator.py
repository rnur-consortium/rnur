#!/usr/bin/env python3
import csv
import sys
import os

def parse_hex(hex_str):
    """Converts a Unicode code point string (e.g., 'U+EE00', 'EE00', '0xEE00') into an integer."""
    clean_str = hex_str.upper().replace('U+', '').replace('0X', '').strip()
    return int(clean_str, 16)

def check_overlap(start1, end1, start2, end2):
    """Returns True if two code point ranges overlap."""
    return max(start1, start2) <= min(end1, end2)

def run_full_database_scan(base_dir):
    """
    Scans the entire existing repository data files (master and sandbox) 
    to ensure internal consistency within each parallel set layer.
    """
    paths = [
        os.path.join(base_dir, 'data', 'set1_master.csv'),
        os.path.join(base_dir, 'data', 'set2_sandbox.csv')
    ]
    allocated = []
    has_errors = False
    
    print("\nExecuting comprehensive RNUR matrix validation scan...")
    
    for path in paths:
        if not os.path.exists(path):
            print(f"[-] CRITICAL ERROR: {path} does not exist.")
            return False
            
        print(f"Analyzing {os.path.basename(path)} for integrity...")
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for line_num, row in enumerate(reader, start=2):
                # Skip checking against open/empty slots
                if row.get('Status') in ['Waiting for Submissions', 'Provisional Allocation / Open for Submission']:
                    continue
                try:
                    s_set = int(row['Set_Number'])
                    start = parse_hex(row['Start_Code_Point'])
                    end = parse_hex(row['End_Code_Point'])
                    
                    # Dynamically key the project/script name due to differing headers
                    script_name = row.get('Script_Name') or row.get('Project_Name') or "UNKNOWN_ITEM"
                    
                    # Parallel Isolation Collision Check
                    for c_file, c_set, c_start, c_end, c_name, c_line in allocated:
                        if s_set == c_set and check_overlap(start, end, c_start, c_end):
                            print(f"[-] CRITICAL COLLISION DETECTED IN SET {s_set}!")
                            print(f"    -> Current:  {os.path.basename(path)}, Line {line_num} ({script_name}) [{hex(start)}-{hex(end)}]")
                            print(f"    -> Existing: {os.path.basename(c_file)}, Line {c_line} ({c_name}) [{hex(c_start)}-{hex(c_end)}]")
                            has_errors = True
                            
                    allocated.append((path, s_set, start, end, script_name, line_num))
                except Exception as e:
                    print(f"[-] Malformed data in {os.path.basename(path)} on line {line_num}: {e}")
                    has_errors = True
                    
        print(f"[+] {os.path.basename(path)} internal verification complete.")
        
    if has_errors:
        print("\n[-] SCAN FAILED: Matrix conflicts or malformed entries detected.")
        return False
        
    print("\n[+] SUCCESS: Entire RNUR matrix verified cleanly with zero internal overlaps.")
    return True

def validate_single_submission(set_number, start_hex, end_hex, master_csv_path):
    """Checks a single new script proposal against the master registry file."""
    if not os.path.exists(master_csv_path):
        print(f"[-] Error: Master registry file not found at {master_csv_path}")
        return False

    try:
        new_start = parse_hex(start_hex)
        new_end = parse_hex(end_hex)
    except ValueError:
        print("[-] Error: Invalid hexadecimal format provided.")
        return False

    if new_start > new_end:
        print("[-] Error: Start code point cannot be greater than the end code point.")
        return False

    collisions = []

    with open(master_csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Status'] in ['Waiting for Submissions', 'Provisional Allocation / Open for Submission']:
                continue            
            try:
                current_set = int(row['Set_Number'])
                if current_set == int(set_number):
                    curr_start = parse_hex(row['Start_Code_Point'])
                    curr_end = parse_hex(row['End_Code_Point'])
                    
                    if check_overlap(new_start, new_end, curr_start, curr_end):
                        collisions.append(row)
            except (ValueError, KeyError):
                continue

    if collisions:
        print(f"\n[!] COLLISION DETECTED in Set {set_number}!")
        for item in collisions:
            name = item.get('Script_Name') or item.get('Project_Name') or "Unknown"
            author = item.get('Author') or item.get('Owner') or "Unknown"
            print(f"  - Script: {name} ({item['Start_Code_Point']} to {item['End_Code_Point']}) by {author}")
        return False

    print(f"\n[+] SUCCESS: Range {start_hex} to {end_hex} in Set {set_number} is valid for entry!")
    return True

if __name__ == "__main__":
    print("=== RNUR Allocation Validator ===")
    
    # Calculate base repository directories
    tools_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(tools_dir)
    master_path = os.path.join(base_dir, 'data', 'set1_master.csv')
    
    # If passed explicit parameters, perform a precision check for a single input
    if len(sys.argv) == 4:
        target_set = sys.argv[1]
        start_pt = sys.argv[2]
        end_pt = sys.argv[3]
        success = validate_single_submission(target_set, start_pt, end_pt, master_path)
        sys.exit(0 if success else 1)
        
    # Default behavior: run a complete automated sweep across all registry sheets
    else:
        print("No input coordinates provided. Shifting to global repository integrity check...")
        success = run_full_database_scan(base_dir)
        sys.exit(0 if success else 1)
