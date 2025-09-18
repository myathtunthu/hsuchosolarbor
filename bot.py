import telebot
from telebot import types
import time
import os

# ==================== YOUR BOT TOKEN ====================
BOT_TOKEN = "8234675036:AAFIWLxSxeaT0-VGt_wUwDySCJbHS_0NTN0"
# ========================================================

bot = telebot.TeleBot(BOT_TOKEN)

print("Bot is starting with the provided token...")

# Store user data temporarily
user_data = {}

# Available solar panel wattages
SOLAR_PANEL_WATTAGES = [100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750]

# Available battery voltages
BATTERY_VOLTAGES = [12, 12.8, 22.8, 24, 25.6, 36, 48, 51.2, 60, 72, 96, 102.4]

# Battery types
BATTERY_TYPES = ["LiFePO4", "Lead-Acid", "Gel"]

# Calculation functions here (same as before)
def calculate_daily_consumption(total_w, hours):
    return total_w * hours

def calculate_battery_size(daily_wh, battery_voltage, battery_type="lifepo4"):
    if battery_type.lower() == "lifepo4":
        dod_factor = 0.8
        battery_ah = (daily_wh / battery_voltage) * (1 / dod_factor)
    elif battery_type.lower() == "gel":
        dod_factor = 0.6
        battery_ah = (daily_wh / battery_voltage) * (1 / dod_factor)
    else:
        dod_factor = 0.5
        battery_ah = (daily_wh / battery_voltage) * (1 / dod_factor)
    return battery_ah, dod_factor

def calculate_solar_panels(daily_wh, panel_wattage, sun_hours=5, efficiency=0.85):
    solar_w = (daily_wh / sun_hours) * (1 / efficiency)
    num_panels = round(solar_w / panel_wattage)
    if num_panels < 1:
        num_panels = 1
    return solar_w, num_panels

def calculate_inverter_size(total_w):
    inverter_w = total_w * 1.3
    return inverter_w

def calculate_charge_controller(solar_w, battery_voltage):
    controller_amps = (solar_w / battery_voltage) * 1.25
    if solar_w <= 1000 and battery_voltage <= 24:
        controller_type = "PWM"
    else:
        controller_type = "MPPT"
    return controller_type, controller_amps

# Bot handlers here (same as before)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        welcome_text = """
☀️ *Hsu Cho Solar Calculator Bot မှ ကြိုဆိုပါတယ်!*
        """
        bot.reply_to(message, welcome_text, parse_mode='Markdown')
    except Exception as e:
        print("Error in start:", e)

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
📖 *အဆင့် ၅ ဆင့်ဖြင့် ဆိုလာစနစ်တွက်ချက်နည်း*
        """
    bot.reply_to(message, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['calculate'])
def start_calculation(message):
    try:
        user_data[message.chat.id] = {}
        msg = bot.reply_to(message, "🔌 *ကျေးဇူးပြု၍ စုစုပေါင်းဝပ်အား (W) ထည့်ပါ:*\n\nဥပမာ: 500", parse_mode='Markdown')
        bot.register_next_step_handler(msg, ask_usage_hours)
    except Exception as e:
        print("Error in calculate:", e)
        bot.reply_to(message, "❌ အမှားတစ်ခုဖြစ်နေပါတယ်")

# Other functions here (same as before)

# Run the bot with error handling
if __name__ == "__main__":
    try:
        # Webhook ရှိရင်ဖျက်ပါ
        bot.remove_webhook()
        time.sleep(2)  # 2 seconds wait
        
        print("Bot is starting with polling method...")
        print("Bot token:", BOT_TOKEN)
        
        # Polling စတင်ပါ
        bot.infinity_polling(timeout=20, long_polling_timeout=20)
        
    except Exception as e:
        print("Bot error:", e)
        print("Restarting bot in 10 seconds...")
        time.sleep(10)
        
        # Auto-restart
        os.execv(sys.executable, ['python'] + sys.argv)