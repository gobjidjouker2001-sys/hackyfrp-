import os
import subprocess
import time

# تعريف الألوان
G = '\033[92m'  # أخضر
R = '\033[91m'  # أحمر
C = '\033[96m'  # سماوي
Y = '\033[93m'  # أصفر
W = '\033[97m'  # أبيض
E = '\033[0m'   # إنهاء

def clear():
    os.system('clear')

def banner():
    print(f"""{C}
  _    _            _           ______             
 | |  | |          | |         |  ____|            
 | |__| | __ _  ___| | ___   _ | |__ _ __ _ __     
 |  __  |/ _` |/ __| |/ / | | ||  __| '__| '_ \    
 | |  | | (_| | (__|   <| |_| || |  | |  | |_) |   
 |_|  |_|\__,_|\___|_|\_\\__, ||_|  |_|  | .__/    
                         __/ |           | |       
   {Y}[ Smart Edition: Auto-Detect Enabled ]{C} |_|       
{E}""")

def get_device_info():
    """وظيفة اكتشاف بيانات الهاتف المتصل تلقائياً"""
    print(f"{Y}[*] جاري فحص الجهاز المتصل...{E}")
    try:
        # قراءة الموديل والبراند وإصدار الأندرويد
        brand = subprocess.getoutput("adb shell getprop ro.product.brand").strip()
        model = subprocess.getoutput("adb shell getprop ro.product.model").strip()
        version = subprocess.getoutput("adb shell getprop ro.build.version.release").strip()
        
        if brand and model:
            print(f"{G}-----------------------------------")
            print(f"[+] الجهاز المكتشف: {brand.upper()} {model}")
            print(f"[+] إصدار الأندرويد: {version}")
            print(f"-----------------------------------{E}")
            return brand.lower()
        else:
            print(f"{R}[!] لم يتم اكتشاف جهاز عبر ADB. تأكد من التوصيل.{E}")
            return None
    except:
        return None

# --- خيارات التخطّي ---

def samsung_logic():
    print(f"{Y}[Samsung Mode] جاري تشغيل ثغرة كود الطوارئ...{E}")
    # تخطي واجهة الإعداد
    subprocess.run(["adb", "shell", "settings", "put", "secure", "user_setup_complete", "1"])
    subprocess.run(["adb", "shell", "settings", "put", "global", "device_provisioned", "1"])
    print(f"{G}[+] تم التخطي بنجاح!{E}")

def generic_fastboot():
    print(f"{R}[Fastboot Mode] جاري مسح قسم FRP...{E}")
    subprocess.run(["fastboot", "erase", "frp"])
    subprocess.run(["fastboot", "reboot"])

# --- القائمة الرئيسية الذكية ---

def main():
    while True:
        clear()
        banner()
        
        # محاولة الاكتشاف التلقائي عند التشغيل
        detected_brand = get_device_info()
        
        print(f"\n{W}--- اختر طريقة التخطي ---{E}")
        print(f"1. {G}Smart Bypass (تخطٍ ذكي بناءً على الجهاز المكتشف){E}")
        print(f"2. {C}Manual Samsung Bypass (*#0*# Mode){E}")
        print(f"3. {C}Manual Fastboot Wipe (أجهزة MTK/SPD){E}")
        print(f"4. {C}Open Browser (MTP Mode){E}")
        print(f"5. {R}Exit{E}")
        
        choice = input(f"\n{Y}Select: {E}")
        
        if choice == '1':
            if detected_brand == 'samsung':
                samsung_logic()
            elif detected_brand in ['xiaomi', 'redmi', 'huawei']:
                print(f"{Y}[*] جهاز {detected_brand} مكتشف. يفضل استخدام وضع Fastboot.{E}")
                time.sleep(2)
            else:
                print(f"{R}[!] لم يتم التعرف على براند محدد تلقائياً.{E}")
                time.sleep(2)
                
        elif choice == '2':
            samsung_logic()
        elif choice == '3':
            generic_fastboot()
        elif choice == '4':
            print(f"{C}[*] جاري محاولة فتح المتصفح...{E}")
            subprocess.run(["adb", "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", "https://google.com"])
        elif choice == '5':
            break
        
        input(f"\n{W}اضغط Enter للعودة للقائمة...{E}")

if __name__ == "__main__":
    main()
