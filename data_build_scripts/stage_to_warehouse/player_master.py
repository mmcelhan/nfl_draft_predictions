import json
import os
import pandas as pd
import sys
sys.path.append("..")
sys.path.append("../../column_matching")
import data_build_scripts.helpers as hlp


def main():

    local_path = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(local_path, "player_master.json"))
    data = json.load(f)

    matching = hlp.return_matching_dict()

    two_up = os.path.abspath(os.path.join(local_path, "../.."))

    source_dir = os.path.join(two_up, data['source'])  # should work in both mac and windows
    target_dir = os.path.join(two_up, data['target'])
    source = os.path.join(source_dir, data['folder'], data['file'])
    df = pd.read_csv(source)

    df['college'] = df['college'].map(hlp.return_college_matching_dict())


    df['first_name'] = df['player'].str.split(' ').str[0]
    df['last_name'] = df['player'].str.split(' ').str[1]
    df['position_group'] = df['pos'].map(matching['position_groups'])
    df['section'] = df['position_group'].map(matching['section'])
    df.rename(columns=data['column_rename'], inplace=True)

    espn_id_df = hlp.return_id_df()
    df = pd.merge(df, espn_id_df, left_on=['last_name', 'college', 'position_group'],
                  right_on=['last_name', 'college', 'position_group'], how='left')

    df = df.assign(fms_id=(df['first_name'] + '_' + df['last_name'] + '_'
                       + df['position_group'] + '_' + "draft_year").astype('category').cat.codes)

    df = df[data['keep_columns']]

    target_folder = os.path.join(target_dir, data['output_folder'])
    hlp.make_folder_if_not_exists(target_folder)
    target = os.path.join(target_folder, data['output_file'])
    df.to_csv(target, index=False)


main()