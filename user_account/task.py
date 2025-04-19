from celery import shared_task
from kavenegar import KavenegarAPI

@shared_task
def send_verification_sms_async(user_number, code):
    try:
        api = KavenegarAPI('78323961326C677677354935544C79543059434A32363451334246456C77507779314F56653943536671633D')
        params = {
            'sender': '2000660110',
            'receptor': user_number,
            'message': f'کد تایید شما: {code}',
        }
        api.sms_send(params)
    except Exception as e:
        print(f'خطا در ارسال پیامک: {e}')
