from fastapi_mail import FastMail,ConnectionConfig,MessageSchema,MessageType
from config.config import settings
from extra.helper_functions import generate_ticket
import tempfile

def make_email_html(buyer:dict,tickets):
    text_tickets=""
    for ticket in tickets:
          text_tickets+=f"""
              <li>
              <h2>
                  <strong>{ticket}</strong>
              </h2>
              </li>
            """
    body=f"""
<html dir="ltr" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">
  <head>
    <meta charset="UTF-8">
    <meta content="width=device-width, initial-scale=1" name="viewport">
    <meta name="x-apple-disable-message-reformatting">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta content="telephone=no" name="format-detection">
    <title></title>
    <!--[if (mso 16)]>
    <style type="text/css">
    a {{text-decoration: none;}}
    </style>
    <![endif]-->
    <!--[if gte mso 9]><style>sup {{ font-size: 100% !important; }}</style><![endif]-->
    <!--[if gte mso 9]>
<xml>
    <o:OfficeDocumentSettings>
    <o:AllowPNG></o:AllowPNG>
    <o:PixelsPerInch>96</o:PixelsPerInch>
    </o:OfficeDocumentSettings>
</xml>
<![endif]-->
  </head>
  <body class="body">
    <div dir="ltr" class="es-wrapper-color">
      <!--[if gte mso 9]>
			<v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t">
				<v:fill type="tile" color="#fafafa"></v:fill>
			</v:background>
		<![endif]-->
      <table width="100%" cellspacing="0" cellpadding="0" class="es-wrapper">
        <tbody>
          <tr>
            <td valign="top" class="esd-email-paddings">
              <table cellpadding="0" cellspacing="0" align="center" class="es-header">
                <tbody>
                  <tr>
                    <td align="center" class="esd-stripe">
                      <table bgcolor="#ffffff" align="center" cellpadding="0" cellspacing="0" width="600" class="es-header-body">
                        <tbody>
                          <tr>
                            <td align="left" class="esd-structure es-p20t es-p20r es-p20l">
                              <!--[if mso]><table width="560" cellpadding="0" cellspacing="0"><tr><td width="270" valign="top"><![endif]-->
                              <table cellpadding="0" cellspacing="0" align="left" class="es-left">
                                <tbody>
                                  <tr>
                                    <td width="270" align="left" class="esd-container-frame es-m-p20b">
                                      <table width="100%" role="presentation" cellpadding="0" cellspacing="0">
                                        <tbody>
                                          <tr>
                                            <td align="center" class="esd-block-image" style="font-size:0">
                                              <a target="_blank">
                                                <img width="270" src="https://elrbbpo.stripocdn.email/content/guids/CABINET_6dfdad7857396b4e26660c822937c1f5261a6890bf76dc2a37000c1c06fed99f/images/udep_logo.png" alt="" class="adapt-img">
                                              </a>
                                            </td>
                                          </tr>
                                        </tbody>
                                      </table>
                                    </td>
                                  </tr>
                                </tbody>
                              </table>
                              <!--[if mso]></td><td width="20"></td><td width="270" valign="top"><![endif]-->
                              <table cellpadding="0" cellspacing="0" align="right" class="es-right">
                                <tbody>
                                  <tr>
                                    <td width="270" align="left" class="esd-container-frame">
                                      <table cellpadding="0" cellspacing="0" width="100%" role="presentation">
                                        <tbody>
                                          <tr>
                                            <td align="center" class="esd-block-image" style="font-size:0">
                                              <a target="_blank">
                                                <img src="https://elrbbpo.stripocdn.email/content/guids/CABINET_6dfdad7857396b4e26660c822937c1f5261a6890bf76dc2a37000c1c06fed99f/images/logoasme1.png" alt="" width="145" class="adapt-img">
                                              </a>
                                            </td>
                                          </tr>
                                        </tbody>
                                      </table>
                                    </td>
                                  </tr>
                                </tbody>
                              </table>
                              <!--[if mso]></td></tr></table><![endif]-->
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </td>
                  </tr>
                </tbody>
              </table>
              <table cellpadding="0" cellspacing="0" align="center" class="es-content">
                <tbody>
                  <tr>
                    <td align="center" class="esd-stripe">
                      <table bgcolor="#ffffff" align="center" cellpadding="0" cellspacing="0" width="600" class="es-content-body">
                        <tbody>
                          <tr>
                            <td align="left" class="esd-structure es-p30t es-p20b es-p20r es-p20l es-m-p20t">
                              <table cellpadding="0" cellspacing="0" width="100%">
                                <tbody>
                                  <tr>
                                    <td width="560" align="center" valign="top" class="esd-container-frame">
                                      <table cellpadding="0" cellspacing="0" width="100%">
                                        <tbody>
                                          <tr>
                                            <td align="center" class="esd-block-text es-p10b">
                                              <h1 class="es-m-txt-c" style="font-size:46px;line-height:100%">
                                                ¡Gracias por participar en nuestra rifa!
                                              </h1>
                                            </td>
                                          </tr>
                                          <tr>
                                            <td align="center" class="esd-block-image es-p10t es-p10b" style="font-size:0px">
                                              <a target="_blank">
                                                <img src="https://elrbbpo.stripocdn.email/content/guids/CABINET_6dfdad7857396b4e26660c822937c1f5261a6890bf76dc2a37000c1c06fed99f/images/image_ybq.png" alt="" width="530" class="adapt-img" style="display: block">
                                              </a>
                                            </td>
                                          </tr>
                                        </tbody>
                                      </table>
                                    </td>
                                  </tr>
                                </tbody>
                              </table>
                            </td>
                          </tr>
                          <tr>
                            <td align="left" class="esd-structure es-p10t es-p10b es-p20r es-p20l">
                              <table cellpadding="0" cellspacing="0" width="100%">
                                <tbody>
                                  <tr>
                                    <td width="560" valign="top" align="center" class="es-m-p0r esd-container-frame">
                                      <table cellspacing="0" width="100%" cellpadding="0">
                                        <tbody>
                                          <tr>
                                            <td align="left" class="esd-block-text es-text-2441">
                                              <h3 class="es-text-mobile-size-24" style="text-align:justify;font-size:24px;line-height:120% !important">
                                                Hola <strong>{buyer["first_name"]}</strong>,
                                              </h3>
                                              <h3 class="es-text-mobile-size-22" style="text-align:justify;font-size:22px;line-height:120% !important">
                                                ¡Muchas felicidades y gracias por comprar tus tickets para la<strong>GRAN RIFA DE ASME</strong>! Nos emociona mucho contar contigo en esta iniciativa, y esperamos que esta oportunidad te acerque a ganar grandes premios.
                                              </h3>
                                            </td>
                                          </tr>
                                        </tbody>
                                      </table>
                                    </td>
                                  </tr>
                                </tbody>
                              </table>
                            </td>
                          </tr>
                          <tr>
                            <td align="left" class="esd-structure es-p20t es-p20r es-p20l">
                              <table width="100%" cellpadding="0" cellspacing="0">
                                <tbody>
                                  <tr>
                                    <td width="560" align="left" class="esd-container-frame">
                                      <table cellpadding="0" cellspacing="0" width="100%" role="presentation">
                                        <tbody>
                                          <tr>
                                            <td align="left" class="esd-block-text">
                                              <h3>
                                                Datos del comprador:
                                              </h3>
                                              <h3>
                                                Nombre: {buyer["first_name"]}
                                              </h3>
                                              <h3>
                                                Apellido: {buyer["last_name"]}
                                              </h3>
                                              <h3>
                                                Correo: {buyer["email"]}
                                              </h3>
                                              <h3>
                                                DNI: {buyer["dni"]}
                                              </h3>
                                              <h3>
                                                Celular: {buyer["cell_phone"]}
                                              </h3>
                                            </td>
                                          </tr>
                                        </tbody>
                                      </table>
                                    </td>
                                  </tr>
                                </tbody>
                              </table>
                            </td>
                          </tr>
                          <tr>
                            <td align="left" class="esd-structure es-p20t es-p20r es-p20l">
                              <table width="100%" cellpadding="0" cellspacing="0">
                                <tbody>
                                  <tr>
                                    <td width="560" align="left" class="esd-container-frame">
                                      <table width="100%" role="presentation" cellpadding="0" cellspacing="0">
                                        <tbody>
                                          <tr>
                                            <td align="left" class="esd-block-text">
                                              <h2>
                                                <strong>Tickets:</strong>
                                              </h2>
                                              <ul>
                                                {text_tickets}
                                              </ul>
                                            </td>
                                          </tr>
                                        </tbody>
                                      </table>
                                    </td>
                                  </tr>
                                </tbody>
                              </table>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </td>
                  </tr>
                </tbody>
              </table>
              <table cellpadding="0" cellspacing="0" align="center" class="es-footer">
                <tbody>
                  <tr>
                    <td align="center" class="esd-stripe">
                      <table align="center" cellpadding="0" cellspacing="0" width="640" class="es-footer-body" style="background-color:transparent">
                        <tbody>
                          <tr>
                            <td align="left" class="esd-structure es-p20t es-p20b es-p20r es-p20l">
                              <table cellpadding="0" cellspacing="0" width="100%">
                                <tbody>
                                  <tr>
                                    <td width="600" align="left" class="esd-container-frame">
                                      <table cellpadding="0" cellspacing="0" width="100%">
                                        <tbody>
                                          <tr>
                                            <td align="center" class="esd-block-social es-p15t es-p15b" style="font-size:0">
                                              <table cellpadding="0" cellspacing="0" class="es-table-not-adapt es-social">
                                                <tbody>
                                                  <tr>
                                                    <td align="center" valign="top" class="es-p40r">
                                                      <a target="_blank" href="https://www.instagram.com/asme.udep/">
                                                        <img title="Instagram" src="https://elrbbpo.stripocdn.email/content/assets/img/social-icons/logo-black/instagram-logo-black.png" alt="Inst" width="55" height="55">
                                                      </a>
                                                    </td>
                                                  </tr>
                                                </tbody>
                                              </table>
                                            </td>
                                          </tr>
                                          <tr>
                                            <td align="center" class="esd-block-text es-p35b es-text-6202">
                                              <h2>
                                                <span class="es-text-mobile-size-18" style="font-size:18px;line-height:150% !important">@2024 COSAI Brand. Todos los derechos reservados.</span>
                                              </h2>
                                            </td>
                                          </tr>
                                        </tbody>
                                      </table>
                                    </td>
                                  </tr>
                                </tbody>
                              </table>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </td>
                  </tr>
                </tbody>
              </table>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </body>
</html>
"""
    return body

mail_config=ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS
)

mail=FastMail(
    config=mail_config
)

def create_message(recipients:list[str],subject:str,body:str,temp_file_paths) -> MessageSchema:
    message=MessageSchema(
        recipients=recipients,
        subject=subject,
        body=body,
        subtype=MessageType.html,
        attachments=temp_file_paths
    )
    return message

async def send_message(recipients:list[str],subject:str,body:str,tickets):
    
    img_tickets=[]

    for ticket in tickets:
        img_tickets.append(generate_ticket(ticket=ticket))

    temp_file_paths=[]

    for img in img_tickets:
      with tempfile.NamedTemporaryFile(delete=False,suffix=".jpg") as temp_file:
          img.save(temp_file,format="JPEG")
          temp_file_paths.append(temp_file.name)

    message=create_message(recipients=recipients,
                        subject=subject,
                        body=body,
                        temp_file_paths=temp_file_paths)
    await mail.send_message(message=message)