import csv
import argparse
from datetime import datetime

class CSVEditor:
    def __init__(self, input_file='time_lines.csv', output_file='updated_time_lines.csv'):
        self.input_file = input_file
        self.output_file = output_file

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CSVファイルにデータを追加します。")
    parser.add_argument('--input', type=str, default='time_lines.csv', help='入力CSVファイルのパス')
    parser.add_argument('--output', type=str, default='updated_time_lines.csv', help='出力CSVファイルのパス')
    args = parser.parse_args()
    # print(args)
    # 入力ファイルと出力ファイルのパスを取得
    input_file = args.input
    output_file = args.output

    # 追加する店舗データの例
    additional_data = [
        ['2023-10-01', '1234567', 'Store B', 'Product X', '150'],
        ['2023-10-02', '1234567', 'Store B', 'Product Y', '200']
    ]

    # CSVEditorクラスを使用してデータを追加
    editor = CSVEditor(input_file, output_file)
    editor.append_store_data(additional_data)

    column_replacements = {
        '店舗': ['hogehoge1']
    }

    # バリエーションデータを追加
    editor.append_variation_data(column_replacements)

    print(f"新しいCSVファイルが作成されました: {output_file}")
    print(f"バリエーションデータが追加され、新しいCSVファイルが作成されました: {output_file}")
