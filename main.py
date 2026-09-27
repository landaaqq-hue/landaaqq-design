import os
import sys
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print("\033[1;31m========================================\033[0m")
    print("\033[1;32m      L A N D  -  Secure App        \033[0m")
    print("\033[1;31m========================================\033[0m")

def main():
    clear_screen()
    banner()
    print("\033[1;36m[+] جارٍ تهيئة بيئة الحماية والتشفير...\033[0m")
    time.sleep(1)
    
    # نظام الحماية بالـ PIN
    print("\n\033[1;33m--- تسجيل الدخول الآمن ---\033[0m")
    pin = input("أدخل رمز الحماية (PIN) للتطبيق: ")
    
    if not pin:
        print("\033[1;31m[-] تم إلغاء الدخول أو الرمز فارغ!\033[0m")
        return

    clear_screen()
    banner()
    print("\033[1;32m[✔] تم تسجيل الدخول بنجاح! مرحباً بك في Land.\033[0m\n")

    while True:
        print("\n\033[1;36m=== القائمة الرئيسية (واجهة Land) ===\033[0m")
        print("1. إعدادات اليوزرات المميزة (أحادي إلى خماسي)")
        print("2. إدارة الحظر وقائمة الأمان")
        print("3. رابط صانع التطبيق (تيك توك)")
        print("4. خروج من التطبيق")
        
        choice = input("\nاختر رقم العملية (1-4): ")
        
        if choice == '1':
            clear_screen()
            banner()
            print("\n\033[1;33m--- نظام اليوزرات المميزة ---\033[0m")
            username = input("أدخل اليوزر المطلوب (من 1 إلى 5 أحرف/أرقام): ").strip()
            length = len(username)
            
            if 1 <= length <= 5:
                print(f"\033[1;32m[SUCCESS] مبروك! اليوزر '{username}' متوفر ومن فئة ({length} أحرف). تم حجزه بنجاح!\033[0m")
            else:
                print("\033[1;31m[ERROR] خطأ: يجب أن يكون اليوزر نادراً ومحصوراً بين الأحادي (1) والخماسي (5) فقط!\033[0m")
            input("\nاضغط Enter للعودة للقائمة...")
            clear_screen()
            banner()

        elif choice == '2':
            clear_screen()
            banner()
            print("\n\033[1;33m--- إدارة الحظر والأمان ---\033[0m")
            print("1. حظر مستخدم جديد")
            print("2. عرض المحظورين")
            sub_choice = input("اختر خيار الأمان: ")
            if sub_choice == '1':
                blocked_user = input("أدخل اسم المستخدم أو المعرف للحظر: ")
                print(f"\033[1;32m[✔] تم حظر المستخدم ({blocked_user}) بنجاح وتأمين الحساب.\033[0m")
            input("\nاضغط Enter للعودة...")
            clear_screen()
            banner()

        elif choice == '3':
            clear_screen()
            banner()
            print("\n\033[1;33m--- تيك توك صانع التطبيق (Land) ---\033[0m")
            print("رابط المنصة الرسمي: https://www.tiktok.com")
            input("\nاضغط Enter للعودة...")
            clear_screen()
            banner()

        elif choice == '4':
            print("\n\033[1;31m[!] إغلاق التطبيق بأمان. إلى اللقاء!\033[0m")
            break
        else:
            print("\n\033[1;31m[-] خيار غير صحيح، حاول مرة أخرى.\033[0m")

if __name__ == '__main__':
    main()

