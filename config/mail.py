from fastapi_mail import FastMail,ConnectionConfig,MessageSchema,MessageType
from config.config import settings
from extra.helper_functions import generate_ticket
import tempfile

def make_email_html(seller:str,buyer:str,ticket):
    event_name="GRAN RIFA ASME"
    body=f"""
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
                            <img src="https://elrbbpo.stripocdn.email/content/guids/CABINET_6dfdad7857396b4e26660c822937c1f5261a6890bf76dc2a37000c1c06fed99f/images/logoasme1.png" alt="" width="560" class="adapt-img" style="display: block">
                          </a>
                        </td>
                      </tr>
                      <tr>
                        <td align="center" class="esd-block-text es-p5t es-p5b es-p40r es-p40l es-m-p0r es-m-p0l">
                          <p style="font-size:16px">
                            ​
                          </p>
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
                          <h2 class="es-text-mobile-size-24" style="text-align: justify; font-size: 24px; line-height: 120% !important">
                            Hola <strong>{buyer}</strong>,
                          </h2>
                          <h2 style="text-align: justify">
                            ​
                          </h2>
                          <h2 class="es-text-mobile-size-22" style="text-align: justify; font-size: 22px; line-height: 120% !important">
                            ¡Muchas felicidades y gracias por comprar tus tickets para la<strong>GRAN RIFA DE ASME</strong>! Nos emociona mucho contar contigo en esta iniciativa, y esperamos que esta oportunidad te acerque a ganar grandes premios.
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
                          <h2>
                            Vendedor: <strong>{seller}</strong>
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
                            <li>
                              <h2>
                                <strong>{ticket}</strong>
                              </h2>
                            </li>
                            <li>
                              <h2>
                                <strong>{ticket}</strong>
                              </h2>
                            </li>
                            <li>
                              <h2>
                                <strong>{ticket}</strong>
                              </h2>
                            </li>
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

def create_message(recipients:list[str],subject:str,body:str,temp_file_path) -> MessageSchema:
    message=MessageSchema(
        recipients=recipients,
        subject=subject,
        body=body,
        subtype=MessageType.html,
        attachments=[temp_file_path]
    )
    return message

async def send_message(recipients:list[str],subject:str,body:str,ticket):
    img_ticket=generate_ticket(ticket=ticket)

    with tempfile.NamedTemporaryFile(delete=False,suffix=".jpg") as temp_file:
        img_ticket.save(temp_file,format="JPEG")
        temp_file_path=temp_file.name

    message=create_message(recipients=recipients,
                        subject=subject,
                        body=body,
                        temp_file_path=temp_file_path)
    await mail.send_message(message=message)