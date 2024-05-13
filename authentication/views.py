import json
from .forms import ProfileForm, UserForm
from django.db import transaction, IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User


def send_email_verification():
    html_message = (
        '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" '
        '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
        '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" '
        'xmlns:o="urn:schemas-microsoft-com:office:office" lang="en">'
        'Neue,Arial,sans-serif;line-height:22px;font-weight:400;font-style:normal;font-size:16px;text-decoration:none'
        ';text-transform:none;letter-spacing:0;direction:ltr;color:#333;text-align:left;mso-line-height-rule:exactly'
        ';mso-text-raise:2px}h1{margin:0;Margin:0;font-family:Roboto,BlinkMacSystemFont,Segoe UI,Helvetica Neue,'
        'Arial,sans-serif;line-height:34px;font-weight:400;font-style:normal;font-size:28px;text-decoration:none;text'
        '-transform:none;letter-spacing:0;direction:ltr;color:#333;text-align:left;mso-line-height-rule:exactly;mso'
        '-text-raise:2px}h2{margin:0;Margin:0;font-family:Lato,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,'
        'sans-serif;line-height:30px;font-weight:400;font-style:normal;font-size:24px;text-decoration:none;text'
        '-transform:none;letter-spacing:0;direction:ltr;color:#333;text-align:left;mso-line-height-rule:exactly;mso'
        '-text-raise:2px}h3{margin:0;Margin:0;font-family:Lato,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,'
        'sans-serif;line-height:26px;font-weight:400;font-style:normal;font-size:20px;text-decoration:none;text'
        '-transform:none;letter-spacing:0;direction:ltr;color:#333;text-align:left;mso-line-height-rule:exactly;mso'
        '-text-raise:2px}</style></head>'
        ''
        '<body id="body" class="t26" style="min-width:100%;Margin:0px;padding:0px;background-color:#F4F4F4;"><div '
        'class="t25" style="background-color:#F4F4F4;"><table role="presentation" width="100%" cellpadding="0" '
        'cellspacing="0" border="0" align="center"><tr><td class="t24" '
        'style="font-size:0;line-height:0;mso-line-height-rule:exactly;background-color:#F4F4F4;" valign="top" '
        'align="center"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" '
        'align="center" id="innerTable"><tr><td><div class="t20" '
        'style="mso-line-height-rule:exactly;font-size:1px;display:none;">&nbsp;</div></td></tr><tr><td><table '
        'class="t22" role="presentation" cellpadding="0" cellspacing="0" '
        'style="Margin-left:auto;Margin-right:auto;"><tr><td class="t21" '
        'style="background-color:#FFFFFF;width:400px;padding:40px 40px 40px 40px;"><table role="presentation" '
        'width="100%" cellpadding="0" cellspacing="0"><tr><td><table class="t2" role="presentation" cellpadding="0" '
        'cellspacing="0" style="Margin-right:auto;"><tr><td class="t1" style="width:55px;padding:0 15px 0 0;"><div '
        'style="font-size:0px;">'
        ''
        '<img class="t0" '
        'style="display:block;border:0;height:auto;width:100%;Margin:0;max-width:100%;" width="55" height="35.78125" '
        'alt="" src="https://873bf0ff-510b-4e56-add9-23f07643d9f2.b-cdn.net/e/7c1b81b5-3da9-4347-857b-565f01b7aac4'
        '/0536ec87-177c-481c-9603-eaad2866556b.png"/>'
        '</div></td></tr></table></td></tr><tr><td><div class="t3" '
        'style="mso-line-height-rule:exactly;mso-line-height-alt:42px;line-height:42px;font-size:1px;display:block'
        ';">&nbsp;</div></td></tr><tr><td><table class="t6" role="presentation" cellpadding="0" cellspacing="0" '
        'style="Margin-left:auto;Margin-right:auto;"><tr><td class="t5" style="width:400px;"><h1 class="t4" '
        'style="margin:0;Margin:0;font-family:Albert Sans,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,'
        'sans-serif;line-height:41px;font-weight:800;font-style:normal;font-size:39px;text-decoration:none;text'
        '-transform:none;letter-spacing:-1.56px;direction:ltr;color:#333333;text-align:left;mso-line-height-rule'
        ':exactly;mso-text-raise:1px;">Confirm your account</h1></td></tr></table></td></tr><tr><td><div class="t7" '
        'style="mso-line-height-rule:exactly;mso-line-height-alt:16px;line-height:16px;font-size:1px;display:block'
        ';">&nbsp;</div></td></tr><tr><td><table class="t10" role="presentation" cellpadding="0" cellspacing="0" '
        'style="Margin-left:auto;Margin-right:auto;"><tr><td class="t9" style="width:400px;"><p class="t8" '
        'style="margin:0;Margin:0;font-family:Albert Sans,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,'
        'sans-serif;line-height:21px;font-weight:400;font-style:normal;font-size:16px;text-decoration:none;text'
        '-transform:none;letter-spacing:-0.64px;direction:ltr;color:#333333;text-align:left;mso-line-height-rule'
        ':exactly;mso-text-raise:2px;">Please click the button below to confirm your email address and finish setting '
        'up your account. This link is valid for 24 hours.</p></td></tr></table></td></tr><tr><td><div class="t12" '
        'style="mso-line-height-rule:exactly;mso-line-height-alt:35px;line-height:35px;font-size:1px;display:block'
        ';">&nbsp;</div></td></tr><tr><td><table class="t14" role="presentation" cellpadding="0" cellspacing="0" '
        'style="Margin-right:auto;"><tr><td class="t13" '
        'style="background-color:#000000;overflow:hidden;width:105px;text-align:center;line-height:34px;mso-line'
        '-height-rule:exactly;mso-text-raise:6px;border-radius:40px 40px 40px 40px;">'
        '<span class="t11" '
        'style="display:block;margin:0;Margin:0;font-family:Inter Tight,BlinkMacSystemFont,Segoe UI,Helvetica Neue,'
        'Arial,sans-serif;line-height:34px;font-weight:900;font-style:normal;font-size:13px;text-decoration:none;text'
        '-transform:uppercase;direction:ltr;color:#FFFFFF;text-align:center;mso-line-height-rule:exactly;mso-text'
        '-raise:6px;">Confirm'
        '</span></td></tr></table></td></tr><tr><td><div class="t17" '
        'style="mso-line-height-rule:exactly;mso-line-height-alt:35px;line-height:35px;font-size:1px;display:block'
        ';">&nbsp;</div></td></tr><tr><td><table class="t19" role="presentation" cellpadding="0" cellspacing="0" '
        'style="Margin-left:auto;Margin-right:auto;"><tr><td class="t18" style="width:400px;"><p class="t16" '
        'style="margin:0;Margin:0;font-family:Albert Sans,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,'
        'sans-serif;line-height:21px;font-weight:400;font-style:normal;font-size:16px;text-decoration:none;text'
        '-transform:none;letter-spacing:-0.64px;direction:ltr;color:#333333;text-align:left;mso-line-height-rule'
        ':exactly;mso-text-raise:2px;">Didn&#39;t register on IR Business Analytic? <a class="t15" '
        'href="https://tabular.email" style="margin:0;Margin:0;font-weight:700;font-style:normal;text-decoration:none'
        ';direction:ltr;color:#2F353D;mso-line-height-rule:exactly;" target="_blank">Click here to let us '
        'know.</a></p></td></tr></table></td></tr></table></td></tr></table></td></tr></table></div>'
        '</body></html>'
    )
    message = ("Confirm your account Please click the button below to confirm your email address and finish setting up "
               "your account. This link is valid for 24 hours.Didn't register on IR Business Analytic? Click here to "
               "let us know.")


# Create your views here.

class Auth(APIView):
    @transaction.atomic
    def post(self, request):
        saved_profile = None
        saved_user = None
        try:
            data = json.loads(request.body)

            userData = {
                "first_name": data['firstname'],
                "last_name": data['lastname'],
                "email": data['email'],
            }
            profileData = {
                "phone": data['phone'],
                "address": data['address'],
                "country": data['country'],
                "position": data['position'],
                "gender": data['gender']
            }

            user = UserForm(userData)
            if user.is_valid():
                saved_user = User.objects.create(email=user.cleaned_data['email'],
                                                 first_name=user.cleaned_data['first_name'],
                                                 last_name=user.cleaned_data['last_name'],
                                                 password=data['password'])
            profile = ProfileForm(profileData)
            if profile.is_valid():
                saved_profile = profile.save(commit=False)
                saved_profile.user = saved_user
                saved_profile.save()
            return Response({"status": 'success', "id": saved_profile.id}, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({"status": 'failed', "code": "email_exist", "msg": str(e)},
                            status=status.HTTP_208_ALREADY_REPORTED)
        except Exception as e:
            return Response({"status": 'failed', "code": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
