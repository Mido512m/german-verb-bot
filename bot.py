import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

# ===== ضع مفاتيحك هنا =====
TELEGRAM_TOKEN = "8781771775:AAFUIVy4vJ5ZXhvadF4FcaXGiC6jsqRAw1c"
GEMINI_API_KEY = "AIzaSyCMey1UnxCM6wY5DgypC7UjBUBoKkpZEWY"
# ===========================

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

PROMPT = """
أنت خبير متخصص في اللغة الألمانية. المستخدم سيعطيك فعلاً ألمانياً.
قدّم التحليل التالي بالتنسيق الدقيق جداً. لا تتخطى أي نقطة.

━━━━━━━━━━━━━━━━━━━━━━━━
🔤 الفعل: [اكتب الفعل بصيغة المصدر]
━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ الترجمة للعربية:
اكتب معاني الفعل المهمة فقط بالعربية

━━━━━━━━━━━━━━━━━━━━━━━━

2️⃣ الاسم المشتق من الفعل:
اكتب الاسم مع أداة التعريف (der/die/das) والجمع
مثال: 
der Kauf 
die Käufe

━━━━━━━━━━━━━━━━━━━━━━━━

3️⃣ أفعال مرادفة (نفس المعنى):
اكتب 2 إلى 4 أفعال مرادفة فقط

━━━━━━━━━━━━━━━━━━━━━━━━

4️⃣ حروف الجر والحالة الإعرابية:
اذا كان الفعل يأتي مع حرف جر ثابت فقط

━━━━━━━━━━━━━━━━━━━━━━━━

5️⃣ الكلمات الشائعة مع الفعل (Kollokationen):
اكتب الكلمات أو الأفعال التي تأتي معه عادة في الألمانية الحقيقية
مثل: etwas kaufen / im Supermarkt kaufen / günstig kaufen
بشرط ان تكون تحت بعضها البعض
━━━━━━━━━━━━━━━━━━━━━━━━

6️⃣ تصريف الفعل الكامل:

🔹 المضارع (Präsens):
ich ___ | du ___ | er/sie/es ___
wir ___ | ihr ___ | sie/Sie ___

🔹 الماضي البسيط (Präteritum):
ich ___ | du ___ | er/sie/es ___
wir ___ | ihr ___ | sie/Sie ___

🔹 الماضي المركب (Perfekt):
haben/sein + [Partizip II]

🔹 Partizip II: ___
🔹 هل الفعل منتظم أم غير منتظم؟ ___

━━━━━━━━━━━━━━━━━━━━━━━━

7️⃣ خمس أمثلة حقيقية على الفعل:
(جمل طويلة نسبياً، من الحياة اليومية الألمانية الحقيقية فقط)

1. [الجملة بالألمانية]
   ↳ [الترجمة بالعربية]

2. [الجملة بالألمانية]
   ↳ [الترجمة بالعربية]

3. [الجملة بالألمانية]
   ↳ [الترجمة بالعربية]

4. [الجملة بالألمانية]
   ↳ [الترجمة بالعربية]

5. [الجملة بالألمانية]
   ↳ [الترجمة بالعربية]

━━━━━━━━━━━━━━━━━━━━━━━━

8️⃣ خمس أمثلة حقيقية على الاسم المشتق:
(جمل طويلة نسبياً، من الحياة اليومية الألمانية الحقيقية فقط)

1. [الجملة بالألمانية]
   ↳ [الترجمة بالعربية]

2. [الجملة بالألمانية]
   ↳ [الترجمة بالعربية]

3. [الجملة بالألمانية]
   ↳ [الترجمة بالعربية]

4. [الجملة بالألمانية]
   ↳ [الترجمة بالعربية]

5. [الجملة بالألمانية]
   ↳ [الترجمة بالعربية]

━━━━━━━━━━━━━━━━━━━━━━━━
تعليمات مهمة جداً:
- كل الأمثلة يجب أن تكون من الحياة اليومية الألمانية الحقيقية
- لا أمثلة جافة أو كتابية فقط
- لا تتخطى أي قسم أبداً
- اكتب بدقة وبشكل منظم
- لا توجد اي نجوم في النص فقط () /
- دئما الترجمة العربية اسفل النص الالماني


"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🇩🇪 *مرحباً! أنا بوت تحليل الأفعال الألمانية*\n\n"
        "أرسل لي أي فعل ألماني وسأعطيك:\n\n"
        "✅ الترجمة الكاملة\n"
        "✅ الاسم المشتق مع أداة التعريف والجمع\n"
        "✅ الأفعال المرادفة\n"
        "✅ حروف الجر والحالات الإعرابية\n"
        "✅ الكلمات الشائعة معه\n"
        "✅ التصريف الكامل\n"
        "✅ 5 أمثلة حقيقية على الفعل\n"
        "✅ 5 أمثلة حقيقية على الاسم\n\n"
        "📝 هذا البوت خاص بالعبقري (عبدالحميد صالح)"
    )
    await update.message.reply_text(text, parse_mode='Markdown')

async def handle_verb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    verb = update.message.text.strip()
    waiting = await update.message.reply_text("⏳ جارٍ التحليل، انتظر لحظة...")
    try:
        full_prompt = f"{PROMPT}\n\nالفعل: {verb}"
        response = model.generate_content(full_prompt)
        result = response.text
        await waiting.delete()

        if len(result) <= 4096:
            await update.message.reply_text(result)
        else:
            parts = []
            temp = result
            while len(temp) > 4096:
                split_at = temp.rfind('\n', 0, 4096)
                if split_at == -1:
                    split_at = 4096
                parts.append(temp[:split_at])
                temp = temp[split_at:]
            parts.append(temp)
            for part in parts:
                await update.message.reply_text(part)
    except Exception as e:
        await waiting.delete()
        await update.message.reply_text(f"❌ حدث خطأ:\n{str(e)}\n\nتأكد من صحة مفاتيح API")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_verb))
    print("✅ البوت يعمل... اضغط Ctrl+C للإيقاف")
    app.run_polling()

if __name__ == "__main__":
    main()