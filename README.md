# Hearthstone Battlegrounds Project

## مستندات

**[مستندات Game Client](./docs/GameClient.md)** - این فایل رو اول از همه بخونید. توش پیدا می‌کنید:
- معماری کامل پروژه
- قوانین بازی و مکانیک `Recruit`/`Combat`
- لیست مینیون‌ها و قابلیت‌هاشون
- ساختار داده‌ها و `Event Log`
- راهنمای انیمیشن و `UI`
- سناریوهای تست

---

## Git Basics

اگه با `Git` .آشنا نیستید، نگران نباشید. اینجا یه توضیح مختصر میدم تا بتونید شروع کنید. اگه قبلاً کار کردید، می‌تونید این بخش رو رد کنید/.

### Git چیه و چرا بهش نیاز داریم؟

`Git` یه سیستم کنترل نسخه است که بهتون امکان میده:
- تاریخچه کامل تغییرات رو داشته باشید
- روی بخش‌های مختلف پروژه به صورت همزمان کار کنید (با `branch`)
- با بقیه همکاری کنید بدون اینکه کار همدیگه رو `overwrite` کنید
- اگه اشتباهی کردید، به نسخه قبلی برگردید

### مفاهیم کلیدی

**Repository (Repo):** یه پوشه که تمام فایل‌های پروژه و تاریخچه تغییرات توشه. می‌تونه `local` (روی کامپیوتر شما) یا `remote` (روی `GitHub`) باشه.

**Branch:** مثل یه خط زمانی جداگانه. شما می‌تونید یه `branch` بسازید، تغییرات بدید، و اگه خوشتون نیومد به `branch` قبلی برگردید. `main` معمولاً `branch` اصلی پروژه است.

**Commit:** یه `snapshot` از تغییرات شما در یه نقطه زمانی. هر `commit` باید یه پیام داشته باشه که می‌گه چی تغییر داده‌اید.

**Fork:** کپی کردن یه `repository` به حساب `GitHub` خودتون. مثل این می‌مونه که یه پروژه رو دانلود کنید و نسخه خودتون رو داشته باشید.

**Pull Request (PR):** راهی برای پیشنهاد دادن تغییرات. شما تغییرات رو توی `fork` یا `branch` خودتون می‌دید، بعد `PR` می‌سازید تا بقیه ببینن و اگه خوب بود `merge` بشه.

### دستورات Git که حتماً باید بلد باشید

این دستورات رو یاد بگیرید، خیلی کارتون راه می‌افته:

```bash
git status
# ببینید چی تغییر کرده

# فایل‌ها رو اضافه کنید به staging (آماده commit شدن)
git add filename.py          # یه فایل خاص
git add .                    # همه فایل‌های تغییر یافته

# تغییرات رو ثبت کنید
git commit -m "Your message here"

# تاریخچه commit ها رو ببینید
git log
git log --oneline            # نسخه کوتاه

# تفاوت‌ها رو ببینید (قبل از commit)
git diff

# بین branch ها جابه‌جا بشید
git checkout branch-name

# یه branch جدید بسازید و بهش برید
git checkout -b new-branch-name

# لیست branch ها رو ببینید
git branch

# تغییرات رو به GitHub بفرستید
git push origin branch-name

# تغییرات رو از GitHub بگیرید
git pull origin branch-name

# فقط تغییرات رو بگیرید (بدون merge کردن)
git fetch origin

# remote repository ها رو ببینید
git remote -v

# یه remote جدید اضافه کنید
git remote add name https://github.com/...

# یه repository رو clone کنید
git clone https://github.com/...

# دو branch رو با هم merge کنید
git merge branch-name
```

### Workflow معمول

یه `workflow` ساده معمولاً این شکله:

1. **کار کنید:** فایل‌ها رو ویرایش کنید
2. **Add کنید:** `git add .` - فایل‌های تغییر یافته رو آماده `commit` کنید
3. **Commit کنید:** `git commit -m "message"` - تغییرات رو ثبت کنید
4. **Push کنید:** `git push` - تغییرات رو به `GitHub` بفرستید

**نکته مهم قبل از `git add .`:**

قبل از اولین `git add .`، مطمئن بشید که فایل `.gitignore` در پروژه وجود داره و شامل موارد زیر است:

```
venv/
__pycache__/
*.pyc
.vscode/
.idea/
.env
*.log
```

این کار باعث می‌شه فایل‌های موقت (مثل محیط مجازی پایتون، فایل‌های کامپایل شده، و تنظیمات `IDE`) `commit` نشن و حجم `repository` کوچیک بمونه.

مثال عملی:
```bash
git status                    # ببینید چی تغییر کرده
git add .                     # همه تغییرات رو اضافه کنید
git commit -m "Deimi - Add new feature"
git push origin student-name  # تغییرات رو push کنید
```

### Tips & Tricks

**قبل از شروع کار هر روز (فقط برای سرگروه):**
```bash
git fetch upstream           # تغییرات جدید رو بگیرید
git checkout main
git merge upstream/main      # با repo اصلی sync بشید
```

**نکته:** فقط سرگروه باید با `upstream` `sync` کند. بقیه اعضا فقط از `branch` تیمی آپدیت می‌گیرند.

**اگه اشتباهی کردید:**
```bash
git checkout -- filename.py
# تغییرات یه فایل رو undo کنید (قبل از commit و قبل از staging)

# فایل رو از staging area بیرون بیارید (Unstage کردن)
git reset HEAD filename.py
# حالا می‌تونید با checkout تغییرات رو دور بریزید:
git checkout -- filename.py

# آخرین commit رو undo کنید (اما تغییرات رو نگه دارید - در حالت Staged)
git reset --soft HEAD~1
# اگر می‌خواید تغییرات Unstaged بشه (یعنی از حالت Staged بیرون بیاد):
git reset HEAD~1  # یا git reset --mixed HEAD~1 (پیش‌فرض)
```

**Commit های کوچک بهترن:** سعی کنید هر `commit` یه کار واحد انجام بده. بهتره ۱۰ تا `commit` کوچک داشته باشید تا یه `commit` بزرگ.

اگه می‌خواید بیشتر یاد بگیرید، [GitHub Guides](https://guides.github.com/) و [Atlassian Git Tutorial](https://www.atlassian.com/git/tutorials) منابع خوبی هستن.

---

## خلاصه Workflow - یک نگاه کلی

قبل از اینکه به جزئیات بریم، اینجا یه خلاصه از `workflow` کلی میدم تا بفهمید چطوری کار می‌کنه:

1. **Fork و Clone:** `Repository` اصلی رو `fork` می‌کنید و به کامپیوتر `clone` می‌کنید
2. **Branch شخصی:** هر کسی یه `branch` شخصی می‌سازه و توش کار می‌کنه
3. **Branch تیمی:** یکی از تیم `branch` تیمی رو می‌سازه که کدهای نهایی تیم اونجاست
4. **کار روزانه:** هر کسی روی `branch` شخصی کار می‌کنه، `commit` می‌کنه، `push` می‌کنه
5. **Merge به تیم:** از طریق `Pull Request` کدهای شخصی رو به `branch` تیمی `merge` می‌کنید
6. **Sync مداوم:** مرتب کدهای `branch` تیمی رو می‌گیرید تا به‌روز بمونید
7. **تحویل:** فقط `branch` تیمی رو تحویل می‌دید

**مهم:** هیچوقت مستقیماً به `branch` تیمی یا `main` `push` نکنید. همه چیز از طریق `Pull Request` انجام می‌شه.

### دیاگرام Workflow

این دیاگرام نشون می‌ده که چطوری کد بین `repository` های مختلف جابه‌جا می‌شه:

![GitHub Workflow Diagram](./bgknowhow-main/dia.png)

**توضیح دیاگرام:**
- **Upstream Repo (قرمز):** `Repository` اصلی که نگه‌داری میشه
- **Origin (آبی):** `Fork` شخصی شما روی `GitHub`
- **Team Repo (سبز):** `Repository` تیمی که `branch` تیمی توشه
- **Your Local Computer (زرد):** کامپیوتر شما که توش کد می‌زنید

**مراحل:**
1. **Fork:** از `Upstream Repo` به `Origin` (ساخت `fork`)
2. **git push:** از `Local Computer` به `Origin` (ارسال تغییرات)
3. **git pull:** از `Team Repo` به `Local Computer` (`sync` کردن کدهای تیم)
4. **Pull Request:** از `Origin` به `Team Repo` (ارسال کد برای `merge`)
5. **Get Updates:** از `Upstream Repo` به `Origin` و `Local Computer` (همگام‌سازی با `repository` اصلی)

---

## راهنمای مرحله‌به‌مرحله

### مرحله ۰: Fork و Setup اولیه

اول از همه باید `repository` اصلی رو `fork` کنید تا یه کپی ازش توی حساب خودتون داشته باشید.

#### گام ۱: Fork در GitHub

1. به صفحه `repository` اصلی برید
2. بالا سمت راست، روی دکمه سبز "Fork" کلیک کنید
3. چند ثانیه صبر کنید تا `fork` بشه
4. بعد از `fork`، به صفحه `repository` خودتون منتقل می‌شید

بعد از `fork`، `URL` شما چیزی شبیه این می‌شه:
```
https://github.com/YOUR-USERNAME/hearthstone-battlegrounds-1
```


#### گام ۲: Clone به کامپیوتر

حالا باید `repository` رو به کامپیوتر خودتون `clone` کنید:

```bash
cd Desktop  # یا هر جای دیگه
# به پوشه‌ای که می‌خواید پروژه رو توش داشته باشید برید

# Repository خودتون رو clone کنید
git clone https://github.com/YOUR-USERNAME/hearthstone-battlegrounds-1.git

# وارد پوشه پروژه بشید
cd hearthstone-battlegrounds-1
```

**Tip:** `URL` رو مستقیماً از صفحه `GitHub` کپی کنید. توی صفحه `repository`، دکمه سبز `Code` رو بزنید و `HTTPS URL` رو کپی کنید.

#### گام ۳: اضافه کردن Upstream Remote

برای اینکه بتونید تغییرات `repository` اصلی رو بگیرید (مثلاً اگه چیزی اضافه کردم)، باید `upstream remote` رو اضافه کنید:

```bash
git remote add upstream https://github.com/ORIGINAL-OWNER/hearthstone-battlegrounds-1.git
# upstream رو اضافه کنید

# بررسی کنید که درست اضافه شده
git remote -v
```

باید دو تا `remote` ببینید:
- `origin` → `repository` `fork` شده شما
- `upstream` → `repository` اصلی

**چرا این کار لازمه؟** چون شما تغییرات `repository` اصلی رو مستقیم نمی‌تونید بگیرید، باید از طریق `upstream` `sync` کنید.

#### گام ۴: همگام‌سازی با Repository اصلی

قبل از شروع هر کار جدید، این کار رو انجام بدید تا کدتون همیشه به‌روز باشه:

```bash
git fetch upstream
# تغییرات repository اصلی رو بگیرید

# به branch main برید
git checkout main

# تغییرات رو merge کنید
git merge upstream/main

# تغییرات رو به fork خودتون هم push کنید
git push origin main
```

**مهم:** این کار رو قبل از شروع کار جدید انجام بدید. اگه این کار رو نکنید و بعد متوجه بشید که `repository` اصلی تغییر کرده، ممکنه `conflict` بگیرید و دردسر پیدا کنید.

---

### مرحله ۱: ساخت Branch شخصی

هر دانشجو باید یه `branch` شخصی برای خودش بسازه. این `branch` فقط مال شماست و توش آزادید هر کاری می‌خواید بکنید.

**چرا branch شخصی لازمه؟**
- هر کسی می‌تونه مستقل کار کنه بدون اینکه کار بقیه رو خراب کنه
- می‌تونید آزادانه `experiment` کنید
- می‌تونید `commit` های زیادی داشته باشید بدون نگرانی
- فقط وقتی آماده بودید، کدتون رو به `branch` تیمی `merge` می‌کنید

**مراحل ساخت:**

```bash
git checkout main
# 1. اول مطمئن بشید روی main هستید

# 2. repository اصلی رو به‌روز کنید (مهم!)
git fetch upstream
git merge upstream/main

# 3. تغییرات رو به fork خودتون push کنید
git push origin main

# 4. حالا branch شخصی خودتون رو بسازید
git checkout -b student-name
# یا با شماره دانشجویی:
git checkout -b 610334567

# 5. branch رو به GitHub push کنید
git push -u origin student-name
```

**نکات مهم:**
- نام `branch` باید شامل نام یا شماره دانشجویی شما باشه (مثلاً `Deimi` یا `610302000`)
- همه `push` ها باید به `origin` (`fork` خودتون) بره، نه `upstream`
- `-u` فقط اولین بار لازمه (`upstream tracking` رو تنظیم می‌کنه، بعدش فقط `git push` کافیه)
- بعد از اینکه `branch` رو ساختید، همیشه روی همون `branch` کار می‌کنید

**نحوه کار روی branch شخصی:**

```bash
git branch
# همیشه اول چک کنید روی کدوم branch هستید

# اگه روی branch دیگه‌ای هستید، برگردید به branch شخصی
git checkout student-name

# حالا می‌تونید کار کنید:
# 1. کد بزنید یا تغییر بدید
# 2. تغییرات رو commit کنید
git add .
git commit -m "Deimi - Add new feature"
git push origin student-name
```

---

### مرحله ۲: تشکیل تیم و ساخت Branch تیمی

بعد از اینکه تیمتون رو تشکیل دادید، باید تصمیم بگیرید که `branch` تیمی روی کدوم `fork` ساخته بشه. `Branch` تیمی جاییه که کدهای نهایی تیم جمع می‌شه.

**چرا branch تیمی لازمه؟**
- همه کدهای تیم در یه جا جمع می‌شه
- می‌تونید ببینید تیم چی کار کرده
- برای تحویل نهایی استفاده می‌شه
- فقط این `branch` رو بررسی می‌کنم

**گزینه ۱: استفاده از Fork یکی از اعضا (پیشنهادی)**

ساده‌ترین راه اینه که یکی از اعضای تیم (مثلاً نفر اول) `fork` خودش رو به عنوان `repository` تیمی استفاده کنه:

```bash

git checkout main
git pull origin main
# نفر اول تیم این کارها رو انجام میده:
# 1. به branch main بره

# 2. branch تیمی رو بسازه
git checkout -b team/robert  # نام تیم خودتون رو بذارید

# 3. به GitHub push کنه
git push -u origin team/robert
```

**چطوری بقیه اعضا دسترسی داشته باشن:**

بعد از اینکه `branch` تیمی ساخته شد، نفر اول باید بقیه اعضا رو به عنوان `Collaborator` اضافه کنه:

1. به `repository` تیمی برید (`fork` نفر اول)
2. Settings → Collaborators → Add people
3. `username` بقیه اعضای تیم رو اضافه کنید
4. اونا باید `invite` رو قبول کنن

**بعد از اضافه شدن به عنوان Collaborator:**

بقیه اعضا باید `remote` رو اضافه کنن:

```bash
git remote add team-fork https://github.com/TEAM-MEMBER-USERNAME/hearthstone-battlegrounds-1.git
# remote fork تیمی رو اضافه کنید

# بررسی کنید
git remote -v

# حالا می‌تونید branch تیمی رو ببینید
git fetch team-fork  # remote branches رو می‌گیره
git checkout -b team/robert team-fork/team/robert  # branch تیمی رو local می‌سازه
```

**نکته:** اینجا `fetch` لازمه تا `remote branches` رو ببینیم، بعد می‌تونیم `checkout` کنیم. این با `pull` فرق داره - `pull` برای گرفتن تغییرات یه `branch` موجوده، اما اینجا داریم `branch` جدید رو `local` می‌سازیم.

**گزینه ۲: ساخت Organization (اختیاری)**

اگه می‌خواید `repository` جداگانه داشته باشید، می‌تونید یه `Organization` بسازید:

1. به `GitHub` برید
2. `New organization` بسازید
3. `Repository` تیمی رو توی `Organization` بسازید
4. همه اعضا رو به `Organization` اضافه کنید

این روش برای تیم‌های بزرگ‌تر یا اگه می‌خواید `repository` مستقل داشته باشید مفیده.

**چند نکته مهم:**
- فقط **یک نفر** از تیم `branch` تیمی رو می‌سازه (معمولاً نفر اول یا `Team Lead`)
- بقیه اعضا باید `fork` خودشون رو داشته باشن
- همه اعضا باید به عنوان `Collaborator` اضافه بشن تا بتونن `PR` بسازن
- بعد از ساخت `branch` تیمی، همه اعضا باید `remote` رو اضافه کنن (مرحله ۵، گام ۴ رو ببینید)

**مسئولیت‌های سرگروه (Team Lead):**
- `sync` کردن `branch` تیمی با `repository` اصلی (`upstream`) فقط با سرگروه است
- بقیه اعضا فقط از `branch` تیمی آپدیت می‌گیرند
- سرگروه در دستورات `Git` باید از `origin` استفاده کند، نه `team-fork`

---

### مرحله ۳: ثبت تیم در README

قبل از شروع کدزنی، تیمتون رو توی `README` ثبت کنید:

1. **فایل تیم رو بسازید:**

   ```bash
   cp teams/TEAM_TEMPLATE.md teams/robert.md
   ```

   یا به صورت دستی: از فایل `TEAM_TEMPLATE.md` یک کپی بگیرید و نامش رو به `robert.md` تغییر بدید.

2. **فایل رو پر کنید:**
   - نام تیم
   - نام `branch` تیمی (`team/robert`)
   - شماره دانشجویی همه اعضا

3. **توی README یه ردیف به جدول اضافه کنید:**
   ```markdown
   | robert | `team/robert` | 610334567، 610334568، 610334569 | teams/robert.md |
   ```

4. **Commit و PR بدید:**
   ```bash
   git checkout student-name
   git add teams/robert.md README.md
   git commit -m "Deimi - Register team robert in README"
   git push origin student-name
   ```

5. **Pull Request بسازید:**
   - به **repository اصلی** برید (نه `fork` خودتون)
   - Pull requests → New pull request
   - "compare across forks" رو بزنید
   - Base: `main` از `repository` اصلی
   - Head: `student-name` از `fork` شما
   - توضیحات `PR` رو بنویسید
   - Create pull request

---

### مرحله ۴: شروع کدزنی - Workflow کامل کار با Git


#### Workflow روزانه - چطوری هر روز کار کنید

**صبح، قبل از شروع کار:**

**برای اعضای عادی تیم:**
```bash
git checkout student-name
# 1. به branch شخصی خودتون برید

# 2. کدهای branch تیمی رو بگیرید (اگه تیم چیزی تغییر داده)
git pull team-fork team/robert
```

**برای سرگروه (Team Lead):**
```bash
git checkout student-name
# 1. به branch شخصی خودتون برید

# 2. کدهای branch تیمی رو بگیرید (از origin استفاده کنید، نه team-fork)
git pull origin team/robert

# 3. repository اصلی رو به‌روز کنید (فقط سرگروه این کار رو می‌کنه)
git fetch upstream
git checkout main
git merge upstream/main
git checkout student-name

# 4. تغییرات upstream رو به branch تیمی هم sync کنید
git checkout team/robert
git merge upstream/main
git push origin team/robert
git checkout student-name
```

**حین کار:**
```bash
git checkout student-name
# 1. همیشه روی branch شخصی خودتون کار کنید

# 2. کد بزنید و تغییرات بدید
# ... کد زدن ...

# 3. تغییرات رو commit کنید
git add .
git commit -m "Deimi - Add new feature"

# 4. به GitHub push کنید
git push origin student-name
```

**چند وقت یکبار کدتون رو به branch تیمی merge کنید:**
- وقتی یه بخش کامل شد
- وقتی یه `feature` آماده شد
- وقتی می‌خواید با تیم `share` کنید
- از طریق `Pull Request` (مرحله ۵ رو ببینید)

#### Workflow کامل از ابتدا تا انتها

یه مثال کامل از `workflow`:

```bash
git checkout student-name
# 1. صبح: شروع کار

# 2. کدهای تیم رو sync کنید
# نکته: اگر سرگروه هستید (صاحب مخزن تیمی)، به جای team-fork از origin استفاده کنید
git pull team-fork team/robert  # یا git pull origin team/robert اگر سرگروه هستید

# 3. کد بزنید
# ... کار می‌کنید ...

# 4. تغییرات رو commit کنید
git add .
git commit -m "Deimi - Add CardSlot component"
git push origin student-name

# 5. بعد از چند commit، PR بسازید (مرحله ۵)
# 6. بعد از merge، دوباره sync کنید
git checkout team/robert
git pull team-fork team/robert  # یا git pull origin team/robert اگر سرگروه هستید
git checkout student-name
git pull team-fork team/robert  # یا git pull origin team/robert اگر سرگروه هستید
```

#### نکات مهم

**همیشه روی branch شخصی کار کنید:**
```bash
git branch
# قبل از شروع کار، چک کنید

# باید * student-name رو ببینید
```

**Commit های مرتب داشته باشید:**
- بعد از هر تغییر کوچک `commit` کنید
- `Commit message` های واضح بنویسید
- `Commit` های کوچک بهتر از `commit` های بزرگ

**Push مرتب:**
- بعد از هر `commit` مهم، `push` کنید
- این کار `backup` محسوب می‌شه
- اگه مشکلی پیش اومد، کدتون روی `GitHub` هست

---

### فرمت Commit Message - خیلی مهمه!

این بخش رو جدی بگیرید. `commit message` های بد می‌تونه برای شما و تیمتون دردسرساز بشه.

#### فرمت استاندارد

```
Last Name - Description of changes
```

همیشه نام فامیلی خودتون رو اول بذارید (بدون کروشه)، بعد یه خط تیره (`-`)، بعد توضیحات.

**نکته:** از کروشه استفاده نکنید. فرمت صحیح: `Last Name - Description` نه `[Last Name] - Description`.

#### مثال‌های درست و غلط

**درست:**
```bash
git commit -m "Deimi - Add CardSlot component for displaying cards"
git commit -m "Mohammadi - Fix drag and drop issue in Recruit Screen"
git commit -m "BMO - Implement Triple and Discover system"
```


#### نکات مهم

1. **نام فامیلی رو همیشه اول بذارید** - اینطوری می‌تونیم ببینیم هر کسی چی کار کرده

2. **توضیحات رو واضح بنویسید:**
   - خوب: `"Deimi - Implement minion purchase system from shop"`
   - بد: `"Deimi - changes"` یا `"Deimi - fix"`

3. **اگه commit شما چند بخش داره، می‌تونید چند خطی بنویسید:**
   ```bash
   git commit -m "Deimi - Add CardSlot component

   - Create CardSlot component for displaying cards
   - Add hover animation
   - Fix responsive issue on mobile"
   ```

4. **Commit های کوچک بهترن:** بهتره چند تا `commit` کوچک داشته باشید تا یه `commit` بزرگ.

#### مثال‌های واقعی برای این پروژه

```bash
# UI Components
git commit -m "Deimi - Create Button component with hover animation"
git commit -m "Deimi - Add LogPanel for displaying event log"

# Game Logic
git commit -m "Mohammadi - Implement minion buy and sell system"
git commit -m "Mohammadi - Add Triple and Golden minion logic"

# Combat System
git commit -m "BMO - Implement attack and damage resolve system"
git commit -m "BMO - Add Deathrattle and Summon logic"

# Server/Backend
git commit -m "Marcus - Create endpoint for minion purchase"
git commit -m "Marcus - Implement WebSocket for combat events"

# Bug Fixes
git commit -m "Hosseini - Fix memory leak in animation system"
git commit -m "Hosseini - Fix index out of range error in board management"

# Documentation
git commit -m "Deimi - Update API documentation"
```

#### چرا این فرمت مهمه؟

- **ردیابی مشارکت:** می‌تونیم ببینیم هر کسی چه کاری انجام داده
- **دیباگ:** اگه مشکلی پیش اومد، می‌تونیم ببینیم کدوم `commit` مشکل داره
- **نمره‌دهی:** برای بررسی مشارکت از `commit history` استفاده می‌شه

**هشدار جدی:** `Commit message` هایی که این فرمت رو نداشته باشن، توی نمره‌دهی تأثیر منفی دارن!

---

### فرمت Pull Request Description

وقتی `PR` می‌سازید، توضیحات `PR` هم باید کامل و واضح باشه. این به `reviewer` کمک می‌کنه سریع‌تر بفهمه چی تغییر داده‌اید.

#### فرمت پیشنهادی

```markdown
**Changes:**
- [توضیح تغییر ۱]
- [توضیح تغییر ۲]
- [توضیح تغییر ۳]

**Tested:**
- [x] تست ۱ انجام شده
- [x] تست ۲ انجام شده

**Notes:**
- [نکات یا هشدارها]
```

#### مثال‌های واقعی

**مثال ۱: اضافه کردن کامپوننت**
```markdown
**Changes:**
- Add CardSlot component for displaying cards
- Implement hover and click animations
- Add keyword display (Taunt, Divine Shield, etc.)

**Tested:**
- [x] Component displays correctly in Recruit Screen
- [x] Animations work properly
- [x] Keywords display correctly

**Notes:**
- Card images should be loaded from `assets/minions/`
```

**مثال ۲: رفع باگ**
```markdown
**Changes:**
- Fix drag and drop issue that was placing cards in wrong slots
- Improve validation for drop target

**Tested:**
- [x] Drag and drop works correctly
- [x] Error displays if slot is full
- [x] Card moves to correct location

**Notes:**
- This change is backward compatible with previous code
```

**مثال ۳: Merge به branch تیمی**
```markdown
**Changes:**
- Add minion purchase system from shop
- Implement Triple and Golden logic
- Add Discover popup

**Tested:**
- [x] Minion purchase with 3 gold works
- [x] Triple triggers correctly
- [x] Discover popup displays and selection works

**Notes:**
- This PR includes 15 commits, all following correct format
- Requires review before merge
```

#### نکات مهم

- همیشه توضیحات واضح بنویسید - چی تغییر دادید و چرا
- چک‌لیست تست رو پر کنید - چه چیزهایی رو تست کردید
- اگه `breaking change` هست، حتماً ذکر کنید

---

### مرحله ۵: Merge کردن به Branch تیمی

وقتی یه بخش کامل شد یا می‌خواید کدتون رو با تیم `share` کنید، باید از طریق `Pull Request` به `branch` تیمی `merge` کنید.

#### گام ۱: Push کردن کد

اول کدتون رو به `fork` خودتون `push` کنید:

```bash
git checkout student-name
# مطمئن بشید روی branch شخصی خودتون هستید

# تغییرات رو commit کنید
git add .
git commit -m "Deimi - Add feature description"
git push origin student-name
```

#### گام ۲: ساخت Pull Request

**اگه branch تیمی روی fork یکی از اعضاست:**

1. به `fork` اون عضو برید (`repository` که `branch` تیمی توشه)
2. Pull requests → New pull request
3. "compare across forks" رو بزنید
4. تنظیمات:
   - **Base repository:** `fork` اون عضو
   - **Base:** `team/robert`
   - **Head repository:** `fork` شما
   - **Compare:** `student-name`
5. توضیحات `PR` رو بنویسید (از فرمت بالا استفاده کنید)
6. Create pull request

**اگه branch تیمی روی Organization است:**

1. به `repository` تیمی برید
2. Pull requests → New pull request
3. Base: `team/robert`
4. Compare: `fork` شما و `student-name`
5. `PR` رو بسازید

#### گام ۳: Review و Merge

- یکی از اعضای تیم `PR` رو `review` می‌کنه
- بعد از تأیید، `merge` می‌کنه

**نکته:** اگه `comment` گذاشتن، حتماً جواب بدید و اگه نیاز بود تغییرات بدید.

#### گام ۴: Sync کردن کدهای محلی

بعد از `merge`، همه اعضای تیم باید کدهای تیمی رو `sync` کنن:

```bash

git remote add team-fork https://github.com/TEAM-MEMBER-USERNAME/hearthstone-battlegrounds-1.git
# اگه branch تیمی روی fork یکی از اعضاست:
# 1. remote اون fork رو اضافه کنید (اگه قبلاً اضافه نکردید)

# 2. به branch تیمی برید و sync کنید
git checkout team/robert
git pull team-fork team/robert  # یا git pull origin team/robert اگر سرگروه هستید

# 3. به branch شخصی برگردید و کدهای تیم رو merge کنید
git checkout student-name
git pull team-fork team/robert  # یا git pull origin team/robert اگر سرگروه هستید
```

**Tip:** این کار رو مرتب انجام بدید (مثلاً هر روز قبل از شروع کار) تا `conflict` نداشته باشید.

---

### مرحله ۶: هماهنگی تیمی

برای جلوگیری از `conflict` و مشکل، چند نکته:

- **قبل از شروع کار روی یه فایل، با تیم هماهنگ کنید** - اگه چند نفر همزمان روی یه فایل کار کنن، `conflict` می‌گیرید
- **هر کسی روی بخش خاصی کار کنه** - مثلاً یکی `UI`، یکی `Logic`، یکی `Server`
- **مرتب کدهای branch تیمی رو sync کنید:**

**نکته مهم:** برای `sync` کردن از `git pull` استفاده کنید. این دستور خودش `fetch` و `merge` رو انجام می‌ده، پس نیازی به اجرای جداگانه نیستن.

```bash
git checkout team/robert
# اگه branch تیمی روی fork یکی از اعضاست:

git pull team-fork team/robert  # یا git pull origin team/robert اگر سرگروه هستید
git checkout student-name
git pull team-fork team/robert  # یا git pull origin team/robert اگر سرگروه هستید
# کدهای تیم رو به branch شخصی خودتون merge کنید
```

**نکته مهم برای سرگروه:**
- اگر شما صاحب مخزن تیمی هستید، به جای `team-fork` از `origin` استفاده کنید
- مسئولیت `sync` کردن `branch` تیمی با `repository` اصلی (`upstream`) فقط با شماست
- بقیه اعضا فقط از `branch` تیمی آپدیت می‌گیرند

**نکته:** اگه `conflict` گرفتید، نگران نباشید. بخش `Troubleshooting` رو ببینید.

---

### مرحله ۷: تحویل نهایی - آماده کردن Branch تیمی برای تحویل

قبل از تحویل، باید مطمئن بشید که `branch` تیمی شما کامل، به‌روز و آماده تحویله.

#### گام ۱: بررسی کامل Branch تیمی

اول از همه باید مطمئن بشید که همه کدها به `branch` تیمی `merge` شدن:

```bash
git checkout team/robert
# به branch تیمی برید

# مطمئن بشید همه تغییرات جدید رو گرفتید
git pull team-fork team/robert  # یا git pull origin team/robert اگه branch تیمی روی fork خودتون هست

# بررسی کنید که همه چیز به‌روزه
git log --oneline
```

#### گام ۲: بررسی Commit History

بررسی کنید که همه اعضای تیم `commit` های معنی‌دار داشته‌ان:

```bash
git log --oneline --all
# تاریخچه commit ها رو ببینید

# ببینید چه کسایی commit داشتن
git shortlog -sn
```

**نکته:** اگه یکی از اعضای تیم `commit` نداره یا `commit` هاش خیلی کمه، با اون صحبت کنید.

#### گام ۳: تست نهایی

قبل از تحویل، حتماً پروژه رو تست کنید:

- [ ] پروژه بدون خطای `syntax` اجرا بشه
- [ ] هیچ خطای `import` وجود نداشته باشه
- [ ] فایل‌های موقت و اضافی `commit` نشده باشن
- [ ] همه فایل‌های لازم موجود باشن

#### گام ۴: بررسی فایل‌های تیم

مطمئن بشید که:
- [ ] فایل تیم توی `teams/<team-name>.md` کامل باشه
- [ ] شماره دانشجویی همه اعضا توی فایل تیم باشه
- [ ] جدول تیم‌ها توی `README` به‌روز باشه

#### گام ۵: بررسی نهایی روی GitHub

بعد از اینکه همه چیز رو بررسی کردید، مطمئن بشید که `branch` تیمی روی `GitHub` هم به‌روز باشه:

**نکته مهم:** اگر تمام مراحل قبل را با `PR` انجام داده‌اید، کد شما روی `GitHub` است. نیازی به `push` مستقیم نیست و این کار ممکن است با قوانین پروژه (`protection rules`) تناقض داشته باشد.

- به صفحه `GitHub repository` تیمی برید
- `برنچ` تیمی را بررسی کنید
- مطمئن بشید که آخرین `commit`‌های همه اعضای تیم در `branch` تیمی موجود است

#### گام ۶: تحویل

**اطلاعاتی که باید بدید:**
1. **نام branch تیمی:** مثلاً `team/robert`
2. **Repository:** `URL` کامل `repository` که `branch` تیمی توشه
   - اگه روی `fork` یکی از اعضاست: `https://github.com/TEAM-MEMBER-USERNAME/hearthstone-battlegrounds-1`
   - اگه روی `Organization` است: `https://github.com/ORG-NAME/hearthstone-battlegrounds-1`
3. **اعضای تیم:** نام و شماره دانشجویی همه اعضا (برای اطمینان)

**مثال:**
```
Branch تیمی: team/robert
Repository: https://github.com/Deimi/hearthstone-battlegrounds-1
اعضا: احمدی (610334567)، محمدی (610334568)، رضایی (610334569)
```

---

## Troubleshooting - حل مشکلات رایج

### مشکل ۱: نمی‌تونم fork کنم

**راه حل:**
- مطمئن بشید که به حساب `GitHub` خودتون `login` کردید
- اگه دکمه `Fork` رو نمی‌بینید، `repository` ممکنه `private` باشه

### مشکل ۲: بعد از fork نمی‌تونم clone کنم

**راه حل:**
```bash
git remote -v
# بررسی کنید URL درست باشه

# اگه مشکل دارید، دوباره clone کنید
cd ..
rm -rf hearthstone-battlegrounds-1
git clone https://github.com/YOUR-USERNAME/hearthstone-battlegrounds-1.git
```

### مشکل ۳: نمی‌تونم به repository اصلی دسترسی داشته باشم

**راه حل:**
```bash
git remote -v
# بررسی کنید upstream اضافه شده

# اگه نیست، اضافه کنید
git remote add upstream https://github.com/ORIGINAL-OWNER/hearthstone-battlegrounds-1.git

# دوباره بررسی کنید
git remote -v
```

### مشکل ۴: وقتی PR می‌سازم، fork خودم رو نمی‌بینم

**راه حل:**
- مطمئن بشید کدتون رو به `fork` خودتون `push` کردید
- توی صفحه `PR`، "compare across forks" رو بزنید
- `Head repository` رو به `fork` خودتون تغییر بدید

### مشکل ۵: Conflict در Merge

این یکی از شایع‌ترین مشکلاته. نگران نباشید، حلش آسونه:

```bash
git checkout student-name
git pull team-fork team/robert
# 1. قبل از merge، همیشه کدهای تیم رو pull کنید

# 2. اگه conflict پیش اومد:
# فایل‌های conflict شده رو باز کنید
# علامت‌های <<<<<< و >>>>>> رو پیدا کنید
# کد درست رو نگه دارید و بقیه رو حذف کنید
# بعد commit کنید

git add .
git commit -m "Deimi - Resolve merge conflict with team branch"
```

**نکته:** اگه نمی‌دونید کدوم درسته، با تیم صحبت کنید. معمولاً باید هر دو بخش رو نگه دارید یا با هم ترکیب کنید.

### مشکل ۶: نمی‌تونم به branch تیمی push کنم

**راه حل:**
- شما **نباید** مستقیماً به `branch` تیمی `push` کنید
- همیشه از طریق `Pull Request` کار کنید
- کدتون رو به `branch` شخصی خودتون `push` کنید و بعد `PR` بسازید

---

## نکات مهم و قوانین

### قوانین اصلی

- هر کسی روی `branch` شخصی خودش کار می‌کنه
- کدها از طریق `PR` به `branch` تیمی `merge` می‌شن
- برای تحویل فقط `branch` تیمی بررسی می‌شه
- **Push مستقیم به `main` ممنوع است**
- **Push مستقیم به `branch` تیمی ممنوع است** (فقط از طریق `PR`)

### نکات قبل از شروع

- قبل از شروع کدزنی، حتماً `docs/Game Client.md` رو کامل بخونید
- کدها باید طبق معماری باشه که توی مستندات نوشته شده
- فایل‌های موقت و اضافی رو `commit` نکنید
- عکس‌های مورد نیاز اکثراً توی [فولدر](./bgknowhow-main/images) موجوده
- فقط ردیف تیم خودتون رو توی جدول تغییر بدید

### همگام‌سازی مداوم

**نکته مهم:** فقط سرگروه باید با `repository` اصلی (`upstream`) `sync` کند. بقیه اعضا فقط از `branch` تیمی آپدیت می‌گیرند.

**برای سرگروه:**
```bash
git fetch upstream && git merge upstream/main
```
بعد از `sync`، تغییرات را به `branch` تیمی هم منتقل کنید و `push` کنید تا بقیه اعضا بتوانند استفاده کنند.

**برای اعضای عادی:**
```bash
git pull team-fork team/robert  # یا git pull origin team/robert اگر سرگروه هستید
```

---

### جدول تیم‌ها

| نام تیم | برنچ تیمی | اعضا (شماره دانشجویی) | لینک فایل تیم |
|---------|-----------|------------------------|---------------|
<<<<<<< HEAD
| مثال | `team/example` | 401234567، 401234568 | [teams/example.md](./teams/example.md) |
| 1 | "team/NULL" | 610300045, 440299102, 610302105 | [teams/NULL](./teams/teams-NULL.md) |

=======
| مثال | `team/example` | 610334567، 610334568 | teams/example.md |
>>>>>>> upstream/main
<!-- ردیف تیم خودتون رو اینجا اضافه کنید -->

---

## لینک‌های مفید

- [مستندات Game Client](./docs/GameClient.md) - حتماً بخونید!
- [مستندات Server-Side](./docs/server.md) - در حال تکمیل (Socket Programming)
- [مستندات Mock Payloads](./data/mock_payloads.md)

---

## سوالات

- **GitHub Issues:** بهترین راه برای سوالات تکنیکی. یه `Issue` در `repository` اصلی باز کنید و سوالتون رو بپرسید. این کار به بقیه هم کمک می‌کنه اگه سوال مشابهی داشته باشن.
- **تلگرام:** برای سوالات خصوصی یا مهم

### قبل از اینکه سوال بپرسید

1. **بخش Troubleshooting رو چک کنید** - خیلی از مشکلات رایج اونجا جواب داده شدن
2. **مستندات رو بخونید** - جواب خیلی از سوالات توی مستندات `Game Client` هست
3. **سوالتون رو واضح بنویسید** - توضیح بدید چه کاری می‌خواید انجام بدید، چه خطایی می‌گیرید، و چه کارهایی تا حالا کردید

### سوالات ممنوع

سوالاتی که می‌تونید خودتون جوابشون رو پیدا کنید، جواب داده نمی‌شن:
- "چطوری Git نصب کنم؟" - این رو باید خودتون گوگل کنید
- "چطوری branch بسازم؟" - همه چیز توی این `README` نوشته شده
- "کد من کار نمی‌کنه" - بدون توضیح بیشتر نمی‌تونیم کمک کنیم
- "این ارور پایتون یعنی چی؟" - ارورهای رایج (مثل `SyntaxError`, `IndentationError`, `NameError`) رو کپی کنید و در گوگل سرچ کنید. ۹۹٪ مواقع جواب تو لینک اول هست
- "چرا import کار نمی‌کنه؟" - مطمئن بشید که محیط مجازی (`venv`) فعاله و پکیج‌ها نصب شدن

**موفق باشید!**