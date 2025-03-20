# FF14のリーヴ納品を自動化するスクリプト
# 暁月のリーヴかつ、ジョブは錬金術師のみ対応、納品物は「巨匠の薬酒」
# 事前に「制作依頼：クンビーラ革張りの魔導書」を受注しておくこと（納品せずに受注したままとする）

import pyautogui
from dotenv import load_dotenv
import os
import argparse
import traceback
import time

preparation_info_text = """
【事前準備】
・Windows版のFF14をウィンドウフルスクリーンで起動していること
・残リーヴ数を確認しておくこと（巨匠の薬酒は足りている？）
・.envファイルに記載されているボタンを登録済みであること
・リーヴ納品窓口の前に立っていること、受注係のグリッグ、納品窓口のアルダイルンが見える位置にカメラを調節していること
・納品窓口のアルダイルンをフォーカスターゲットしていること
・受注係のグリッグの近くに立っていること、かつアルダイルンにも話しかけられる位置にいること
・ジョブが錬金術師であること
・「制作依頼：クンビーラ革張りの魔導書」を受注していること（納品せずに受注したままにする）
・巨匠の薬酒のアイテム位置を1番目に移動していること
"""


load_dotenv()
env_data = dict(os.environ)
# Initialize constants from .env
FF14_INIT_DISPLAY_CLICK_X = int(env_data["FF14_INIT_DISPLAY_CLICK_X"])
FF14_INIT_DISPLAY_CLICK_Y = int(env_data["FF14_INIT_DISPLAY_CLICK_Y"])

FF14_DISPLAY_WIDTH = int(env_data["FF14_DISPLAY_WIDTH"])
FF14_DISPLAY_HEIGHT = int(env_data["FF14_DISPLAY_HEIGHT"])

FF14_OK_BUTTON = env_data["FF14_OK_BUTTON"]
FF14_ESC_BUTTON = env_data["FF14_ESC_BUTTON"]
FF14_CURSOR_UP = env_data["FF14_CURSOR_UP"]
FF14_CURSOR_DOWN = env_data["FF14_CURSOR_DOWN"]
FF14_CURSOR_LEFT = env_data["FF14_CURSOR_LEFT"]
FF14_TARGET_NEAR_NPC = env_data["FF14_TARGET_NEAR_NPC"]
FF14_TARGET_FOCUS_NPC = env_data["FF14_TARGET_FOCUS_NPC"]


# リーヴ受注フェーズ
def leve_order_operation():
    # /targetnpcでグリッグをターゲットにする
    pyautogui.press(FF14_TARGET_NEAR_NPC)
    # 決定ボタンでグリッグに話しかける 会話テキストが出てくるまでの待機時間を設定
    pyautogui.press(FF14_OK_BUTTON, interval=0.5)
    # 会話テキストを進める
    pyautogui.press(FF14_OK_BUTTON)
    # 要件は？のウィンドウで「製作稼業」を選択する（下選択1回、決定ボタン1回）
    pyautogui.press(FF14_CURSOR_DOWN)
    pyautogui.press(FF14_OK_BUTTON)
    # リーヴ選択ウィンドウが表示されている
    # Level 88の暁月リーヴがデフォルトで選択されている
    # 今回はLevel 86のリーヴを選択する（上選択2回、決定ボタン3回）
    pyautogui.press(FF14_CURSOR_UP)
    pyautogui.press(FF14_CURSOR_UP)
    pyautogui.press(FF14_OK_BUTTON)
    pyautogui.press(FF14_OK_BUTTON)
    pyautogui.press(FF14_OK_BUTTON)
    # 受注ボタンにカーソルが合っている状態のはずなので、受注ボタンを押す
    pyautogui.press(FF14_OK_BUTTON)
    # Escキーでメインメニューに戻る(2回)
    pyautogui.press(FF14_ESC_BUTTON)
    pyautogui.press(FF14_ESC_BUTTON)


def leve_delivery_operation():
    # /target <f>でフォーカスターゲットしているアルダイルンをターゲット
    pyautogui.press(FF14_TARGET_FOCUS_NPC)
    # 決定ボタンで話しかける（ウィンドウが出てくるまでのインターバルを設ける）
    pyautogui.press(FF14_OK_BUTTON, interval=0.5)
    # どのリーヴを納品するか選択するウィンドウが表示されている
    # 「製作依頼：品質を高める錬金薬」を選択する（左選択1回、下選択1回、決定ボタン1回 （左選択1回入れるのはキー入力操作を受け付けるため））
    pyautogui.press(FF14_CURSOR_LEFT)
    pyautogui.press(FF14_CURSOR_DOWN)
    pyautogui.press(FF14_OK_BUTTON, interval=0.5)  # 会話テキストが出てくるまでの待機時間を設定
    # 会話テキストを進める
    pyautogui.press(FF14_OK_BUTTON, interval=0.5)  # ウィンドウが出てくるまでの待機時間を設定
    # 製作依頼の納品ウィンドウが表示されている
    # 納品アイテムを選択して渡すボタンを押す（決定ボタン5回（納品アイテム選択→所持品ウィンドウに移動→薬酒選択→渡すボタン選択→HQクオリティの注意書きに対してOKボタンを押す））
    pyautogui.press(FF14_OK_BUTTON)
    pyautogui.press(FF14_OK_BUTTON)
    pyautogui.press(FF14_OK_BUTTON)
    pyautogui.press(FF14_OK_BUTTON, interval=0.5)  # 会話テキストが出てくるまでの待機時間を設定
    # 会話テキストを進めて納品完了（決定ボタン3回）
    pyautogui.press(FF14_OK_BUTTON)
    pyautogui.press(FF14_OK_BUTTON)
    pyautogui.press(FF14_OK_BUTTON)


if __name__ == "__main__":

    try:
        parser = argparse.ArgumentParser(description="FF14 Auto Leve Clicker")
        parser.add_argument(
            "levecount",
            type=int,
            help="リーヴ納品をしたい回数(1-100)を入力してください",
        )
        args = parser.parse_args()

        if not 1 <= args.levecount <= 100:
            print("リーヴ納品回数は1-100の間で指定してください")
            exit(1)

    except Exception as e:
        print(f"エラーが発生しました：{e}")
        exit()

    print(preparation_info_text)
    print("リーヴ納品の自動実行を行いますか？(y/n)")
    answer = input()
    if answer == "y":
        print("リーヴ納品を自動実行します")
    else:
        print("実行を中止します")

    try:
        # FF14の画面を表示するため、FF14のウィンドウをアクティブにする（INITの座標へマウスカーソルを移動する）
        pyautogui.FAILSAFE = (
            False  # 画面左上をマウスクリックしたいため、FAILSAFEをFalseにする
        )
        init_x = int(FF14_INIT_DISPLAY_CLICK_X)
        init_y = 0  # 画面右上をクリックするため、y座標は0
        pyautogui.click(init_x, init_y, interval=1.0)
        # FAILSAFEに引っかからないように、FF14のウィンドウの真ん中にマウスカーソルを移動する
        pyautogui.click(int(FF14_DISPLAY_WIDTH) / 2, 0, interval=1.0)

        pyautogui.FAILSAFE = (
            True  # FF14のウィンドウをアクティブにした後は、FAILSAFEをTrueに戻す
        )
        pyautogui.PAUSE = 0.5  # クリック後の待機時間

        print("リーヴ納品オペレーションを開始します")
        leve_count = args.levecount
        for i in range(leve_count):
            print(f"{i+1}回目のリーヴ納品を開始します")

            # -----------------------------------------------
            # リーヴ受注フェーズ
            # -----------------------------------------------
            leve_order_operation()

            # -----------------------------------------------
            # リーヴ納品フェーズ
            # -----------------------------------------------
            leve_delivery_operation()

            # ここまでリーヴ納品は完了、次のリーヴ納品に進む
            print(f"{i+1}回目のリーヴ納品が完了しました")

            # リーヴ納品の間隔を設ける
            time.sleep(1)

        print("リーヴ納品オペレーションがすべて完了しました")

    except Exception as e:
        traceback.print_exc()
