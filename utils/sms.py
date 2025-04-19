from kavenegar import KavenegarAPI, APIException, HTTPException


def send_verification_sms(user_number, code):
    try:
        api = KavenegarAPI('78323961326C677677354935544C79543059434A32363451334246456C77507779314F56653943536671633D')
        params = {
            'sender': '2000660110',
            'receptor': user_number,
            'message': f'کد تایید شما: {code}',
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print('API Exception:', e)
    except HTTPException as e:
        print('HTTP Exception:', e)
