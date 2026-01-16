#!/bin/bash

# تعريف الألوان لتنسيق المخرجات
C='\033[0;36m'
G='\033[0;32m'
Y='\033[1;33m'
R='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${C}-------------------------------------------${NC}"
echo -e "${G}      HackyFrp - Setup & Launcher        ${NC}"
echo -e "${C}-------------------------------------------${NC}"

# 1. التحقق من صلاحيات الجذر (Root)
if [ "$EUID" -ne 0 ]; then 
  echo -e "${R}[!] يرجى التشغيل بصلاحيات sudo${NC}"
  exit
fi

# 2. تثبيت التبعيات إذا كانت مفقودة
echo -e "${Y}[*] جاري فحص وتثبيت الأدوات المطلوبة (ADB/Fastboot)...${NC}"
apt-get update -y > /dev/null
apt-get install adb fastboot python3-pip -y > /dev/null

# 3. إعداد قواعد USB (udev rules) للتعرف على الهواتف
echo -e "${Y}[*] تهيئة منافذ USB للتعرف على الأجهزة...${NC}"
sudo usermod -aG plugdev $USER

# 4. إعادة تشغيل خادم ADB لضمان الاتصال
echo -e "${Y}[*] جاري تشغيل خادم ADB...${NC}"
adb kill-server
adb start-server

# 5. التأكد من وجود ملف البايثون الأساسي
if [ ! -f "HackyFrp.py" ]; then
    echo -e "${R}[!] خطأ: ملف HackyFrp.py غير موجود في هذا المجلد!${NC}"
    exit
fi

# 6. منح صلاحية التشغيل لملف البايثون
chmod +x HackyFrp.py

echo -e "${G}[+] كل شيء جاهز. جاري تشغيل الأداة...${NC}"
sleep 2

# تشغيل الأداة
python3 HackyFrp.py
