import pandas as pd
import glob

def get_location():
    ground_truth = glob.glob(os.path.join('<PATH>', 'File_*'))
    return ground_truth

def get_column_data():
    all_truth = list()
    for index in range(len(ground_truth)):
        data = pd.read_csv(ground_truth[index], names=['Number','Timestamp','CAN_ID','Length','DLC','Truth'])
        truth = data['Truth']
        all_truth.append(truth)
    return all_truth

def concat_truth(all_truth):
    df = pd.concat([all_truth[0],all_truth[1],all_truth[2],all_truth[3]], ignore_index=True)
    return df


def write_result(new_df):
    df.to_csv('./result.csv', mode='a')
        

if __name__ == '__main__':
    ground_truth = get_location()
    all_truth = get_column_data()
    df = concat_truth(all_truth)

    new_df = pd.DataFrame(df)
    # print (new_df)
    write_result(new_df)

    # df = pd.read_csv('./result.csv')
    # print (df.shape)