import os
from multiprocessing import Pool
import time
from aws_encryption_sdk import StrictAwsKmsMasterKeyProvider, KMSMasterKey
import aws_encryption_sdk

def encrypt_file(file_path):
    try:
        # encryption logic
        return (file_path, True, None)
    except Exception as e:
        return (file_path, False, str(e))

def batch_files_by_data_amount(files, batch_data_amount):
    batches = []
    current_batch = []
    current_batch_size = 0

    for file in files:
        file_size = os.path.getsize(file)
        if current_batch_size + file_size <= batch_data_amount:
            current_batch.append(file)
            current_batch_size += file_size
        else:
            batches.append(current_batch)
            current_batch = [file]
            current_batch_size = file_size
    if current_batch:
        batches.append(current_batch)
    return batches

def generate_report(user_id, start_time, end_time, results):
    processed_files = [r[0] for r in results if r[1]]
    failed_files = [(r[0], r[2]) for r in results if not r[1]]

    total_runtime_seconds = end_time - start_time
    runtime_hours = int(total_runtime_seconds / 3600)
    runtime_minutes = (total_runtime_seconds % 3600) / 60

    report = {
        'user_id': user_id,
        'start_time': start_time,
        'end_time': end_time,
        'runtime_hours': runtime_hours,
        'runtime_minutes': runtime_minutes,
        'total_processed_files': len(processed_files),
        'count_failed_files': len(failed_files),
        'number_of_batches': len(results),
        'failed_files': failed_files
    }
    
    # Print report to screen
    for key, value in report.items():
        if key != "failed_files":
            print(f"{key}: {value}")
        else:
            print("Failed files:")
            for file, reason in value:
                print(f" - {file} | Reason: {reason}")

    # Write report to a .txt file
    with open('encryption_report.txt', 'w') as f:
        for key, value in report.items():
            if key != "failed_files":
                f.write(f"{key}: {value}\n")
            else:
                f.write("Failed files:\n")
                for file, reason in value:
                    f.write(f" - {file} | Reason: {reason}\n")

def process_files(files, user_id):
    NUM_CORES = 4  # Adjust based on your EC2 instance
    BATCH_DATA_AMOUNT = 1024 * 1024 * 100  # 100 MB; adjust as needed

    batches = batch_files_by_data_amount(files, BATCH_DATA_AMOUNT)

    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    with Pool(processes=NUM_CORES) as pool:
        results = pool.map(encrypt_file, [file for batch in batches for file in batch])
    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    
    generate_report(user_id, start_time, end_time, results)

if __name__ == "__main__":
    FILES_TO_PROCESS = ['/path/to/file1', '/path/to/file2', ...]  # Provide your list of files here
    USER_ID = 'User123'  # Provide your user id here
    process_files(FILES_TO_PROCESS, USER_ID)
