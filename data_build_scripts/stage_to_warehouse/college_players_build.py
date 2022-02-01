import json
import os
import pandas as pd
import sys
sys.path.append("..")
sys.path.append("../../column_matching")
import data_build_scripts.helpers as hlp


def main():
    school_matching = hlp.return_college_matching_dict()

    local_path = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(local_path, "college_players_build.json"))
    data = json.load(f)
    hlp.return_college_matching_dict()

    matching = hlp.return_matching_dict()

    two_up = os.path.abspath(os.path.join(local_path, "../.."))

    source_dir = os.path.join(two_up, data['source'])  # should work in both mac and windows
    target_dir = os.path.join(two_up, data['target'])
    source = os.path.join(source_dir, data['folder'], data['file'])
    df = pd.read_csv(source)
    df['full_name'] = df[['first_name', 'last_name']].astype(str).apply(' '.join, axis=1)
    df['position_group'] = df['position'].map(matching['position_groups'])
    df['section'] = df['position_group'].map(matching['section'])
    df.rename(columns=data['column_rename'], inplace=True)
    df = df[data['column_order']]

    df['college'] = df['college'].map(school_matching).fillna(df['college']).map(matching['college']).fillna(
        df['college'])

    target_folder = os.path.join(target_dir, data['output_folder'])
    hlp.make_folder_if_not_exists(target_folder)
    target = os.path.join(target_folder, data['output_file'])
    df.to_csv(target, index=False)


main()