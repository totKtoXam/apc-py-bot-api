class VkKeyboardButtonType():
    """ Возможные типы кнопки """

    #: Кнопка с текстом
    TEXT = "text"

    #: Кнопка с местоположением
    LOCATION = "location"

    #: Кнопка с оплатой через VKPay
    VKPAY = "vkpay"

    #: Кнопка с приложением VK Apps
    VKAPPS = "open_app"

    #: Кнопка с ссылкой
    OPENLINK = "open_link"

# def get_and_set_messge():
#     if ()


class VkKeyboardButtonColor():
    """ Возможные цвета кнопок """

    #: Синяя
    PRIMARY = 'primary'

    #: Белая
    SECONDARY = 'secondary'

    #: Красная
    NEGATIVE = 'negative'

    #: Зелёная
    POSITIVE = 'positive'
