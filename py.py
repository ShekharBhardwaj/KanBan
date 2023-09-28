import os
import csv

def analyze_directory(directory_path, extension_list):
    # Initialize counters and dictionaries
    total_files = 0
    total_size = 0
    extension_counts = {}
    extension_sizes = {}
    skipped_extensions = {}
    skipped_files_size = 0
    encryption_rate = 0.2833  # GB/minute

    # Convert extension list to lowercase
    extension_list = [ext.lower() for ext in extension_list]

    # Walk through directory
    for dirpath, dirnames, filenames in os.walk(directory_path):
        for filename in filenames:
            total_files += 1
            ext = os.path.splitext(filename)[1].lower()  
            file_size = os.path.getsize(os.path.join(dirpath, filename)) / (1024 * 1024)  # Size in MB
            total_size += file_size

            # Update extension count and size
            if ext in extension_list:
                extension_counts[ext] = extension_counts.get(ext, 0) + 1
                extension_sizes[ext] = extension_sizes.get(ext, 0) + file_size
            else:
                skipped_files_size += file_size
                skipped_extensions[ext] = skipped_extensions.get(ext, 0) + 1

    # Summary for user
    total_encryption_time = (total_size / 1024) / encryption_rate
    print(f"Total files: {total_files}")
    print(f"Total size: {total_size:.2f} MB")
    print(f"Estimated time to process all files: {total_encryption_time:.2f} minutes\n")

    ready_files_count = sum(extension_counts.values())
    ready_files_size = sum(extension_sizes.values())
    ready_encryption_time = (ready_files_size / 1024) / encryption_rate
    print(f"Total files ready for encryption: {ready_files_count}")
    print(f"Total size of files ready for encryption: {ready_files_size:.2f} MB")
    print(f"Estimated encryption time: {ready_encryption_time:.2f} minutes\n")

    print("Detailed report for files ready for encryption:")
    for ext, count in extension_counts.items():
        ext_size = extension_sizes[ext]
        ext_time = (ext_size / 1024) / encryption_rate
        print(f"Extension: {ext} | Files: {count} | Size: {ext_size:.2f} MB | Estimated time: {ext_time:.2f} minutes")

    print("\nSkipped extensions:")
    for ext, count in skipped_extensions.items():
        print(f"Extension: {ext} | Files: {count}")

    skipped_time = (skipped_files_size / 1024) / encryption_rate
    print(f"\nTime saved by skipping: {skipped_time:.2f} minutes")

    # Write to CSV
    with open('directory_analysis.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Attribute', 'Value'])
        writer.writerow(['Total files', total_files])
        writer.writerow(['Total size (MB)', f"{total_size:.2f}"])
        writer.writerow(['Estimated processing time (minutes)', f"{total_encryption_time:.2f}"])
        writer.writerow([])
        writer.writerow(['Total files ready for encryption', ready_files_count])
        writer.writerow(['Total size of files ready (MB)', f"{ready_files_size:.2f}"])
        writer.writerow(['Estimated encryption time (minutes)', f"{ready_encryption_time:.2f}"])
        writer.writerow([])
        writer.writerow(['Extension', 'File count', 'Size (MB)', 'Estimated time (minutes)'])
        for ext, count in extension_counts.items():
            ext_size = extension_sizes[ext]
            ext_time = (ext_size / 1024) / encryption_rate
            writer.writerow([ext, count, f"{ext_size:.2f}", f"{ext_time:.2f}"])
        writer.writerow([])
        writer.writerow(['Skipped Extension', 'File count'])
        for ext, count in skipped_extensions.items():
            writer.writerow([ext, count])
        writer.writerow([])
        writer.writerow(['Time saved by skipping (minutes)', f"{skipped_time:.2f}"])

    print("\nResults written to directory_analysis.csv")

# Test
directory_to_analyze = "/path/to/your/directory"
extensions_to_check = ['.txt', '.pdf']  
analyze_directory(directory_to_analyze, extensions_to_check)
