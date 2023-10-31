import os
import pandas as pd

def update_expiry_dates(file_paths, new_expiry_date, csv_path, user_id, jira_story):
    # Load the expiry date CSV into a DataFrame
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        columns = ['FilePath', 'ExpiryDate', 'LastRequest', 'CurrentRequest', 'JiraStory', 'counter', 'available']
        df = pd.DataFrame(columns=columns)

    statuses = []

    for path in file_paths:
        # Check if path exists in the DataFrame
        if path in df['FilePath'].values:
            index = df[df['FilePath'] == path].index[0]
            
            # Update the expiry date if needed
            if df.at[index, 'ExpiryDate'] < new_expiry_date:
                df.at[index, 'ExpiryDate'] = new_expiry_date
                status = 'Updated expiry date'
            else:
                status = 'Expiry date not updated'
            
            # Update other fields as specified
            df.at[index, 'LastRequest'] = df.at[index, 'CurrentRequest']
            df.at[index, 'CurrentRequest'] = user_id
            df.at[index, 'counter'] += 1
            if df.at[index, 'JiraStory'] != jira_story:
                df.at[index, 'JiraStory'] = jira_story
            
        else:
            status = 'Path not in CSV'

        # Check if the file path exists on the drive
        if not os.path.exists(path):
            status = 'Path not found'
        
        # Only add valid statuses (excluding "Path not found")
        if status != 'Path not found':
            statuses.append((path, status))

    # Update the CSV with any changes
    df.to_csv(csv_path, index=False)

    # Return a DataFrame with file paths and their statuses
    result_df = pd.DataFrame(statuses, columns=['FilePath', 'Status'])
    return result_df

# Example usage
file_paths = ['path1.txt', 'path2.txt']
new_expiry_date = '10/30/2023'
csv_path = 'expiry_dates.csv'
user_id = 'userID123'
jira_story = 'JIRA-456'

result = update_expiry_dates(file_paths, new_expiry_date, csv_path, user_id, jira_story)
print(result)