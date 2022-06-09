
# Production hosts may not have an explicit stage but will contain a .
prod = lambda host: 'stg' not in host and 'dev' not in host and '.' in host
prd = prod

DEFAULT_ARG_RULES = {
  'prod': prod,
  'prd': prd,
}

# Pad 1-digit searches to avoid matching multiple digit numbers
# 1 should match 01 but not 10
def generate_digit_rule(digit):
    return lambda host: '0' + digit in host
for digit in range(1, 10):
    DEFAULT_ARG_RULES[str(digit)] = generate_digit_rule(str(digit))

# Only match cron or db results if they are explicitly requested
cron = lambda argv: next((arg for arg in argv if 'cron' in arg), None) is not None
db = lambda argv: next((arg for arg in argv if 'db' in arg), None) is not None

DEFAULT_HOST_RULES = {
    'cron': cron,
    'db': db,
}

