from detect_dnf import detect

from .capture import capture
from .match import match
import math


class Recogbot(object):

    def __init__(self):
        pass

    def _match_max_val(self, target, img):
        # 获取屏幕截图
        img = img if img is not None else capture()
        # 检测目标位置
        max_val, img, top_left, right_bottom = match(img, f'./game/scene/{target}.png')
        max_val = 1 if max_val > 1 and not math.isinf(max_val) else max_val
        print(f'【模板匹配】 {target} {max_val} {top_left}')
        return max_val

    def _recog(self, target, img=None):
        return 0.99 < self._match_max_val(target, img) <= 1

    def _recog_if(self, target1, target2, img=None):
        max_val = self._match_max_val(target1, img)
        if 0.99 < max_val <= 1:
            return True
        max_val = self._match_max_val(target2, img)
        return 0.99 < max_val <= 1

    def _recog_low_precision(self, target, img=None):
        max_val = self._match_max_val(target, img)
        return 0.94 < max_val <= 1

    def _recog_low_precision_if(self, target, target2, img=None):
        max_val = self._match_max_val(target, img)
        if 0.94 < max_val <= 1:
            return True
        max_val = self._match_max_val(target2, img)
        return 0.99 < max_val <= 1

    def _recog_cheap(self, target, img=None):
        max_val = self._match_max_val(target, img)
        return 0.9 < max_val <= 1

    def _recog_diy_precision(self, target, low, height=1, img=None):
        max_val = self._match_max_val(target, img)
        return low <= max_val <= height

    def detect(self):
        pred, names = detect()
        result = {}
        for s in ['lion', 'boss', 'avatar', 'next', 'bag', 'tutorial', 'skip', 'lion_entry', 'combo', 'door', 'passing',
                  'box', 'close', 'switch', 'menu', 'setting', 'buff', 'jump', 'result', 'skill', 'demon']:
            result[s] = (False, 0, 0)
        for i, det in enumerate(pred):
            if len(det) < 1:
                continue
            for *xyxy, conf, cls in reversed(det):
                x, y = (int(xyxy[0]) * 2, int(xyxy[1]) * 2)
                if names[int(cls)] == 'avatar' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】检测到小可爱")
                    result['avatar'] = (True, x, y)
                if names[int(cls)] == 'skip' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】检测到动画")
                    result['skip'] = (True, x, y)
                if names[int(cls)] == 'boss' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】检测到大Boss")
                    result['boss'] = (True, x, y)
                if names[int(cls)] == 'lion' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】检测到狮子头")
                    result['lion'] = (True, x, y)
                if names[int(cls)] == 'lion_entry' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】检测到狮子头入口", (x, y))
                    result['lion_entry'] = (True, x, y)
                if names[int(cls)] == 'bag' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】检测到背包", (x, y))
                    result['bag'] = (True, x, y)
                if names[int(cls)] == 'next' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】检测到下个任务", (x, y))
                    result['next'] = (True, x, y)
                if names[int(cls)] == 'tutorial' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】检测到游戏教程", (x, y))
                    result['tutorial'] = (True, x, y)
                if names[int(cls)] == 'combo' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】连击数", (x, y))
                    result['combo'] = (True, x, y)
                if names[int(cls)] == 'door' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】连击数", (x, y))
                    result['door'] = (True, x, y)
                if names[int(cls)] == 'close' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】检测到菜单关闭按钮", (x, y))
                    result['close'] = (True, x, y)
                if names[int(cls)] == 'switch' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】检测到角色切换按钮", (x, y))
                    result['switch'] = (True, x, y)
                if names[int(cls)] == 'menu' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】检测到菜单按钮", (x, y))
                    result['menu'] = (True, x, y)
                if names[int(cls)] == 'buff' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】检测到角色Buff", (x, y))
                    result['buff'] = (True, x, y)
                if names[int(cls)] == 'jump' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】检测到跳跃按钮", (x, y))
                    result['jump'] = (True, x, y)
                if names[int(cls)] == 'setting' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】检测到设置按钮", (x, y))
                    result['setting'] = (True, x, y)
                if names[int(cls)] == 'box' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】检测到宝箱", (x, y))
                    result['box'] = (True, x, y)
                if names[int(cls)] == 'demon' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】检测到深渊恶魔", (x, y))
                    result['demon'] = (True, x, y)
                if names[int(cls)] == 'passing' and float(f'{conf:.2f}') > 0.8:
                    print("【实时检测】检测到传送门", (x, y))
                    result['passing'] = (True, x, y)
                if names[int(cls)] == 'result' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】检测到战斗结果", (x, y))
                    result['result'] = (True, x, y)
                if names[int(cls)] == 'skill' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】检测到技能按钮", (x, y))
                    result['skill'] = (True, x, y)
        return result

    def start_game(self):
        return self._recog_if('choose', 'choose_kr')

    def town(self):
        return self._recog('mail')

    def reward(self):
        return self._recog('reward')

    def replay(self):
        return self._recog_low_precision_if('replay', 'replay_kr')

    def clear(self):
        return self._recog('go')

    def skill_back(self):
        return self._recog_if('skill_back', "skill_back_kr")

    def daily_confirm_grey(self):
        return self._recog_if("valley_confirm_grey", "valley_confirm_grey_kr")

    def daily_confirm(self):
        return self._recog_if("valley_confirm", "valley_confirm_kr")

    def daily_valley(self):
        return self._recog('valley')

    def daily_valley_completed(self):
        return self._recog('valley_completed')

    def daily_town(self):
        return self._recog_if('valley_town', 'valley_town_kr')

    def daily_south(self):
        return self._recog('south')

    def daily_south_completed(self):
        return self._recog('south_completed')

    def daily_result(self):
        return self._recog('daily_result')

    def daily_goblin(self):
        return self._recog('goblin')

    def daily_goblin_completed(self):
        return self._recog('goblin_completed')

    def daily_carbon(self):
        return self._recog('carbon')

    def daily_carbon_completed(self):
        return self._recog('carbon_completed')

    def entry_snow_mountain(self):
        return self._recog('adventure_snow_mountain_entry')

    def dead(self):
        return self._recog_if('dead', 'dead_kr')

    def lion_clear(self):
        return self._recog('lion_clear')

    def confirm(self):
        return self._recog_if('confirm', 'confirm_kr') or self._recog_if('confirm2', 'confirm2_kr')

    def next_agency(self):
        return self._recog('next_agency')

    def next_agency_confirm(self):
        return self._recog('next_agency_confirm')

    def equip(self):
        return self._recog_if('equip', 'equip_kr')

    def insufficient_balance(self):
        return self._recog_low_precision_if('insufficient_balance', 'insufficient_balance_kr')

    def insufficient_balance_entry(self):
        return self._recog_low_precision('insufficient_balance_entry')

    def insufficient_balance_demon(self):
        return self._recog_low_precision('insufficient_balance_demon')

    def agency_mission_confirm(self):
        return self._recog_if('agency_mission_confirm', 'agency_mission_confirm_kr')

    def next_agency_none(self):
        return self._recog('next_none')

    def agency_mission_get(self):
        return self._recog_if('agency_mission_get', 'agency_mission_get_kr')

    def skill(self, target):
        return self._recog_low_precision('skills/' + target)

    def close(self):
        return self._recog('close') or self._recog('close2') or self._recog('close3')

    def heaven_mission_receive(self):
        return self._recog_if('heaven_mission_receive', 'heaven_mission_receive_kr')

    def black_town_stuck(self):
        return self._recog_cheap('black_town_stuck')

    def heaven_stuck(self):
        return self._recog_diy_precision('heaven_stuck1', 0.92) or self._recog_diy_precision('heaven_stuck2', 0.92)

    def talk_skip(self):
        return self._recog_low_precision_if('talk_skip_kr', 'talk_skip')

    def union_sign(self):
        return self._recog('guild_sign')

    def union_box1_signed(self):
        return self._recog_diy_precision('guild_signed_coin', 0.97)

    def union_box2_signed(self):
        return self._recog_diy_precision('guild_signed_pill', 0.97)

    def union_box3_signed(self):
        return self._recog_diy_precision('guild_signed_carbon', 0.97)

    def union_box4_signed(self):
        return self._recog_diy_precision('guild_signed_book', 0.97)

    def union_box5_signed(self):
        return self._recog_diy_precision('guild_signed_book', 0.97)

    def union_box_signed(self, index):
        fun_name = "union_box{}_signed".format(index + 1)
        fun = getattr(self, fun_name)
        return fun()

    def revival_coin_received(self):
        return self._recog_if('mall_coin_received', "mall_coin_received_kr")

    def revival_coin_status(self):
        return self._recog("mall_price") and self._recog_if("mall_purchase", "mall_purchase_kr")

    def disrepair(self):
        return self._recog('disrepair')

    def get_all(self):
        return self._recog_if('get_all', 'get_all_kr')

    def achievement_daily_sella(self):
        return self._recog('achievement_daily_sella')

    def achievement_daily_active(self):
        return self._recog_if('achievement_daily_active', 'achievement_daily_active_kr')

    def achievement_weekly_active(self):
        return self._recog_if('achievement_weekly_active', 'achievement_weekly_active_kr')

    def achievement_daily_box(self):
        return self._recog('achievement_daily_3') or self._recog('achievement_daily_6') or self._recog(
            'achievement_daily_9')

    def achievement_weekly_box(self):
        return self._recog('achievement_weekly_2') or self._recog('achievement_weekly_4') or self._recog(
            'achievement_weekly_6') or self._recog('achievement_weekly_8') or self._recog('achievement_weekly_10')

    def in_mail(self):
        return self._recog_if('mail_self', 'mail_self_kr')

    def mail_receive(self):
        return self._recog_if('mail_receive', 'mail_receive_kr')

    def mail_received(self):
        return self._recog_if('mail_received', 'mail_received_kr')

    def recog_any(self, target):
        return self._recog(target)

    def has_empty_cell(self):
        img = capture(640, 0, 640, 800)
        return self._recog('empty_cell', img)

    def replay_prop(self):
        return self._recog_if('replay_prop', 'replay_prop_kr')

    def sm_boss_entry(self):
        return self._recog_low_precision('sm_boss_entry')

    def gang_vault_active(self):
        return self._recog_if('gang_vault_active', 'gang_vault_active_kr')

    def get_one(self):
        return self._recog_if('get_one', 'get_one_kr')

    def duel_chance(self, num):
        return self._recog(f'duel_chance_{num}')

    def duel_reward(self):
        return self._recog('duel_reward')

    def duel_get_all(self):
        return self._recog_if('duel_get_all', 'duel_get_all_kr')

    def duel_get_all_grey(self):
        return self._recog_if('duel_get_all_grey', 'duel_get_all_grey_kr')

    def duel_day_active(self):
        return self._recog_if('duel_day_active', 'duel_day_active_kr')

    def duel_week_active(self):
        return self._recog_if('duel_week_active', 'duel_week_active_kr')

    def duel_season_over(self):
        return self._recog_if('duel_season_over', 'duel_season_over_kr')

    def duel_skill_title(self):
        return self._recog_if('duel_skill_title', 'duel_skill_title_kr')

    def duel_ai_fight(self):
        return self._recog('duel_ai_fight')

    def duel_promotion(self):
        return self._recog('duel_promotion')

    def back(self):
        return self._recog('back')

    def level(self):
        return self._recog_low_precision_if('level', 'level_kr')

    def mail_self_active(self):
        return self._recog_if('mail_self_active', 'mail_self_active_kr')

    def mail_self(self):
        return self._recog_if('mail_self', 'mail_self_kr')

    def home(self):
        return self._recog('home')

    def overweight(self):
        return self._recog('overweight')

    def consumable_active(self):
        return self._recog('consumable_active')

    def csb_onekey(self):
        return self._recog_if('csb_onekey', 'csb_onekey_kr')

    def csb_use(self):
        return self._recog_if('csb_use', 'csb_use_kr')

    def csb_use_large(self):
        return self._recog_if('csb_use_large', 'csb_use_large_kr')

    def back_share(self):
        return self._recog_if('back_share', 'back_share_kr')

    def daily_stage_active(self, stage):
        return self._recog_if(f'daily_stage_active_{stage}', f'daily_stage_active_{stage}_kr')

    def duel_no_target(self):
        return self._recog_if('duel_no_target', 'duel_no_target_kr')

    def daily_map_entry(self):
        return self._recog('daily_right')

    def daily_resistance(self):
        return self._recog('daily_carbon_resistance') or self._recog('daily_goblin_resistance')

    def in_daily(self):
        return self._recog_if('daily_back', 'daily_back_kr')

    def pet(self):
        return self._recog('pet')

    def pet_decompose_btn(self):
        return self._recog_if('pet_decompose_btn', 'pet_decompose_btn_kr')

    def pet_decompose(self):
        return self._recog('pet_decompose')

    def pet_gear(self):
        return self._recog_if('pet_gear', 'pet_gear_kr')

    def pet_gear_active(self):
        return self._recog_if('pet_gear_active', 'pet_gear_active_kr')

    def pet_in_decompose(self):
        return self._recog('pet_in_decompose')

    def pet_lot_empty(self):
        return self._recog('pet_lot_empty')

    def mail_overflow_pet_gear(self):
        for i in range(6):
            if self._recog(f'pet_gear_{i}'):
                return True
        return False
