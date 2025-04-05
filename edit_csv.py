import csv
import argparse
from datetime import datetime

class CSVEditor:
    def __init__(self, input_file='time_lines.csv', output_file='updated_time_lines.csv', output_encoding='utf-8-sig'):
        """
        """
        self.input_file = input_file
        self.output_file = output_file
        self.output_encoding = output_encoding
        

    def append_store_data(self, additional_store_data):
        """
        入力CSVに別の店舗のデータを追加し、新しいCSVファイルとして保存します。

        :param additional_store_data: 追加する店舗データのリスト（各行はリスト形式）
        """
        # 入力CSVを読み込み
        with open(self.input_file, mode='r', encoding='utf-8') as infile:
            reader = list(csv.reader(infile))
            header = reader[0]
            rows = reader[1:]

        # 追加データを行末に追加
        for row in additional_store_data:
            rows.append(row)

        # 新しいCSVファイルとして保存
        with open(self.output_file, mode='w', encoding='utf-8', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(header)  # ヘッダーを書き込み
            writer.writerows(rows)  # データを書き込み

    def append_variation_data(self, column_replacements):
        """
        入力CSVの内容に対して、別の列バリエーションのデータを作成し、それをCSVの末尾に追加します。

        :param date_mapping: 日付の置き換えマッピング（元の日付: 新しい日付のリスト）
        :param column_replacements: 列の置き換え辞書（列名: 一律に置き換える値）
        """
        # 入力CSVを読み込み
        row_index_dict = {}
        with open(self.input_file, mode='r', encoding='utf-8') as infile:
            reader = list(csv.reader(infile))
            header = reader[0]
            for hidx, hstr in enumerate(header):
                row_index_dict[hstr] = hidx
            rows = reader[1:]

        # バリエーションデータを生成
        for key, list1 in column_replacements.items():
            for elem in list1:
                variation_rows = []
                for row in rows:
                    new_row = row.copy()
                    hidx = row_index_dict[key]
                    new_row[hidx] = elem
                    print(new_row)
                    row_index_dict[key]
                    variation_rows.append(new_row)
                    # print(row)
                # 元のデータにバリエーションデータを追加
                rows.extend(variation_rows)

        # 新しいCSVファイルとして保存
        with open(self.output_file, mode='w', encoding='utf-8', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(header)  # ヘッダーを書き込み
            writer.writerows(rows)  # データを書き込み

    def _write_output_csv(self, header, rows):
        with open(self.output_file, mode='w', encoding=self.output_encoding, newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(header)
            writer.writerows(rows)

    def _ret_input_csv(self):
        row_index_dict = {}
        with open(self.input_file, mode='r', encoding='utf-8') as infile:
            reader = list(csv.reader(infile))
            header = reader[0]
            for hidx, hstr in enumerate(header):
                row_index_dict[hstr] = hidx
            rows = reader[1:]

        return header, rows, row_index_dict

    def _get_series_dict(self, series_name, header, rows):
        series_indices = [header.index(name) for name in series_name]
        series_dict = {}
        series_line_num = 0
        print(series_indices)
        for row in rows:
            series_list = []
            for ridx, rvalue in enumerate(row):
                if ridx in series_indices:
                    series_list.append(rvalue)
            if len(series_list) == 2:
                fstr1 = series_list[0]
                fstr2 = series_list[1]
                
                if not fstr1 in series_dict:
                    series_dict[fstr1] = {}
                if not fstr2 in series_dict[fstr1]:
                    series_dict[fstr1][fstr2] = []
                    series_line_num += 1
                
                series_dict[fstr1][fstr2].append(row)
        return series_dict, series_line_num, series_indices


    def expand_series(self, series_name, series_variation_dict):
        header, rows, row_index_dict = self._ret_input_csv()
        series_dict, series_line_num, series_indices = self._get_series_dict(series_name, header, rows)

        new_rows = []

        for key, sub_dict in series_dict.items():
            # 10店舗
            for rindex1 in range(0, 10):
            # 40商品
                for rindex2 in range(0, 40):
                    print([rindex1, rindex2])
                    for sub_key, sub_list in sub_dict.items():
                        for row in sub_list:
                            # new_row = row.copy() 
                            new_row = row.copy()
                            for sidx in series_indices:
                                rvalue = row[sidx]
                                if sidx == 0:
                                    rvalue = rvalue + f'{rindex1}'
                                elif sidx == 1:
                                    new_row[sidx] = rvalue + f'{rindex2}'
                            new_rows.append(new_row)
                        break

        self._write_output_csv(header, new_rows)


    def add_column(self, series_name, key_value_dict):
        """列を追加します
        Args:
            series_name (list): 系列を示す列名を格納する配列（最大2要素）
            key_value_dict (dict): 追加する列名と値の辞書 {列名: [値の配列]}

        Raises:
            ValueError: series_nameが2要素を超える場合
            ValueError: key_value_dictの値の配列が系列の長さを超える場合
        """
        if len(series_name) > 2:
            raise ValueError("series_nameは2要素以下である必要があります")

        # CSVファイルの読み込み
        row_index_dict = {}
        with open(self.input_file, mode='r', encoding='utf-8') as infile:
            reader = list(csv.reader(infile))
            header = reader[0]
            for hidx, hstr in enumerate(header):
                row_index_dict[hstr] = hidx
            rows = reader[1:]

        # series_nameの列インデックスを取得
        # {series_name1: {}, series_name2:{} }        
        series_indices = [header.index(name) for name in series_name]
        series_dict = {}
        series_line_num = 0
        print(series_indices)
        for row in rows:
            series_list = []
            for ridx, rvalue in enumerate(row):
                if ridx in series_indices:
                    series_list.append(rvalue)
            if len(series_list) == 2:
                fstr1 = series_list[0]
                fstr2 = series_list[1]
                
                if not fstr1 in series_dict:
                    series_dict[fstr1] = {}
                if not fstr2 in series_dict[fstr1]:
                    series_dict[fstr1][fstr2] = []
                    series_line_num += 1
                
                series_dict[fstr1][fstr2].append(row)
        
        new_rows = []
        key1_index = 0
        total_index = 0
        for key, sub_dict in series_dict.items():
            key2_index = 0
            for sub_key, sub_list in sub_dict.items():
                for row in sub_list:
                    #　追加していきます。
                    for inc_key, inc_dict in key_value_dict.items():
                        for target_key, value_list in inc_dict.items():
                            if inc_key in series_name:
                                sidx = series_name.index(inc_key)
                                if sidx == 0:
                                    new_value = value_list[key1_index]
                                elif sidx == 1:
                                    new_value = value_list[key2_index]                    
                                else:
                                    new_value = 0
                            elif '(+W+)' in inc_key:
                                new_value = value_list[total_index]

                            if not target_key in header:
                                header.append(target_key)
                            print([key, sub_key, inc_key, new_value, key1_index, key2_index, total_index])
                            row.append(new_value)
                    new_rows.append(row)
                    # print(row)
                key2_index += 1
                total_index += 1

            key1_index += 1
        
        self._write_output_csv(header, new_rows)        
        # print(series_dict)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CSVファイルにデータを追加します。")
    parser.add_argument('--input', type=str, default='time_lines.csv', help='入力CSVファイルのパス')
    parser.add_argument('--output', type=str, default='updated_time_lines.csv', help='出力CSVファイルのパス')
    parser.add_argument('--output-encoding', type=str, default='utf-8-sig', help='出力CSVふぁいるのencoding')
    args = parser.parse_args()
    # print(args)
    # 入力ファイルと出力ファイルのパスを取得
    input_file = args.input
    output_file = args.output
    output_encoding = args.output_encoding

    # 追加する店舗データの例
    additional_data = [
        ['2023-10-01', '1234567', 'Store B', 'Product X', '150'],
        ['2023-10-02', '1234567', 'Store B', 'Product Y', '200']
    ]

    # CSVEditorクラスを使用してデータを追加
    editor = CSVEditor(input_file, output_file, output_encoding)
    editor.append_store_data(additional_data)

    column_replacements = {
        '店舗': ['hogehoge1']
    }

    series_name = ['店舗', '商品']

    column_replacements = {
        '店舗': {'郵便番号2': ['722-0215', '240-0022'] }, 
        '店舗(+W+)商品': {'郵便番号3': ['722-0001', '240-0002'] },
    }

    # 系列を増やします。コピーするんです。

    series_variation = {
        '店舗': 10,
        '商品': 40,
    }


    # editor.expand_series(series_name, series_variation)
    editor.add_column(series_name, column_replacements)
    # バリエーションデータを追加
    # editor.append_variation_data(column_replacements)

    print(f"新しいCSVファイルが作成されました: {output_file}")
    print(f"バリエーションデータが追加され、新しいCSVファイルが作成されました: {output_file}")
