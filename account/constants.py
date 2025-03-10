VERIFIED = 'verified'
ACTIVATED = 'activated'
SUSPENDED = 'suspended'

STATUS_CHOICES = (
    (VERIFIED, "Verified (Can't Login)"),
    (ACTIVATED, "Activated (Can Login)"),
    (SUSPENDED, "Suspended (Can't Transfer)"),
)

PROCESSING = 'Processing'
PENDING = 'Pending'
FAIL = 'Fail'

TRANSFER_CHOICES = (
    (PROCESSING, 'Processing'),
    (PENDING, 'Pending'),
    (FAIL, 'Fail'),
)


MALE = 'M'
FEMALE = 'F'
OTHER = 'O'

GENDER_CHOICE = (
    (MALE, "Male"),
    (FEMALE, "Female"),
    (OTHER, "Other"),
)


DOLLAR = '$'
EURO = '€'
POUNDS = '£'
YEN = 'JPY'
RUPEE = 'INR'
WON = '₩'

CURRENCY_CHOICE = (
    (DOLLAR, "Dollar"),
    (EURO, "Euro"),
    (POUNDS, "British Pounds"),
    (YEN, "Japanese Yen"),
    (RUPEE, "Indian Rupee"),
    (WON, "Korean Won KRW"),
)


BEGINNER = '20,000 +'
AVERAGE = '50,000 +'
ADVANCE = '100,000 +'
ADVANCEPLUS = '200,000 +'
STELLA = '300,000 +'
STELLAPLUS = '400,000 +'
TOP = '500,000 +'

MONEY_CHOICE = (
    (BEGINNER, "20,000 +"),
    (AVERAGE, "50,000 +"),
    (ADVANCE, "100,000 +"),
    (ADVANCEPLUS, "200,000 +"),
    (STELLA, "300,000 +"),
    (STELLAPLUS, "400,000 +"),
    (TOP, "500,000 +"),
)


MR = 'Mr.'
MRS = 'Mrs.'
MISS = 'Miss.'
DR = 'Dr.'
ENGR = 'Engr.'
PROF = 'Prof.'

TITLE_CHOICE = (
    (MR, 'Mr.'),
    (MRS, 'Mrs.'),
    (MISS, 'Miss.'),
    (DR, 'Dr.'),
    (ENGR, 'Engr.'),
    (PROF, 'Prof.')
)


YES = 'LOGIN OTP YES'
NO = 'LOGIN OTP NO'

OTP_CHOICES = (
    (YES, 'LOGIN OTP YES'),
    (NO, 'LOGIN OTP NO')
)