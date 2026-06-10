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

def validate_submission(set_number, start_hex, end_hex, master_csv_path):
    """Checks a new script proposal against the master registry file for coordinate collisions."""
    if not os.path.exists(master_csv_path):
        print(f"[-] Error: Master registry file not found at {master_csv_path}")
        return False

    try:
        new_start = parse_hex(start_hex)
        new_end = parse_hex(end_hex)
    except ValueError:
        print("[-] Error: Invalid hexadecimal format provided for the code points.")
        return False

    if new_start > new_end:
        print("[-] Error: Start code point cannot be greater than the end code point.")
        return False

    collisions = []

    with open(master_csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Skip checking against unallocated placeholder rows
            if row['Status'] == 'Waiting for Submissions':
                continue
            
            try:
                current_set = int(row['Set_Number'])
                # Only check collisions within the exact same parallel set layer
                if current_set == int(set_number):
                    curr_start = parse_hex(row['Start_Code_Point'])
                    curr_end = parse_hex(row['End_Code_Point'])
                    
                    if check_overlap(new_start, new_end, curr_start, curr_end):
                        collisions.append(row)
            except (ValueError, KeyError):
                # Skip malformed or header rows gracefully
                continue

    if collisions:
        print(f"\n[!] COLLISION DETECTED in Set {set_number}!")
        print("The proposed range overlaps with the following existing allocations:\n")
        for item in collisions:
            print(f"  - Script: {item['Script_Name']} ({item['Start_Code_Point']} to {item['End_Code_Point']}) by {item['Author']}")
        return False

    print(f"\n[+] SUCCESS: Range {start_hex} to {end_hex} in Set {set_number} is completely valid and conflict-free!")
    return True

if __name__ == "__main__":
    print("=== RNUR Allocation Validator ===")
    
    # Simple interactive mode if run without arguments
    if len(sys.argv) < 4:
        print("\nUsage: python validator.py [Set_Number] [Start_Code_Point] [End_Code_Point]")
        print("Example: python validator.py 1 U+EE10 U+EE4A\n")
        print("Running in interactive mode...")
        
        target_set = input("Enter Target Set Number (e.g., 1): ").strip()
        start_pt = input("Enter Start Code Point (e.g., U+EE10): ").strip()
        end_pt = input("Enter End Code Point (e.g., U+EE4A): ").strip()
    else:
        target_set = sys.argv[1]
        start_pt = sys.argv[2]
        end_pt = sys.argv[3]

    # Path routing to find the master layout relative to the tool location
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    master_path = os.path.join(base_dir, 'data', 'set1_master.csv')

    success = validate_submission(target_set, start_pt, end_pt, master_path)
    sys.exit(0 if success else 1)
