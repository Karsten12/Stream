import telegram
from telegram.ext import Updater, CommandHandler
from telegram import InputMediaPhoto
import cv2
import io
import lib.utils as utils
from functools import partial
import logging


def check_authorized(update, detector_obj):
    """ Check if the telegram user is authorized

    Args:
        detector_obj ([type]): [description]

    Returns:
        [bool]: T if authorized, F otherwise
    """
    return update.effective_chat.id in detector_obj.telegram_ids


def vacation_mode(update, context, detector_obj):
    """Enable/disable vacation mode when the command /vacation is issued"""
    if not check_authorized(update, detector_obj):
        return
    # TODO


def view_frames(update, context, detector_obj):
    """ Send frame(s) from all cameras (default) or a single camera, when the command /view <cam-name> is issued """
    if not check_authorized(update, detector_obj):
        return
    if context.args:
        if "help" in context.args:
            msg = (
                f"The list of cameras are: {list(detector_obj.ip_cam_objects.keys())}."
            )
            context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
        elif context.args[0] in detector_obj.ip_cam_objects:
            # Send a frame from a single camera
            img = detector_obj.ip_cam_objects[context.args[0]].read_single_frame()
            # change from png to jpg to reduce load times
            buff = cv2.imencode(".jpg", img)[1]
            io_buf = io.BytesIO(buff)
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=io_buf)
    else:
        # Send frames from all cameras
        images = []
        for cam in detector_obj.ip_cam_objects:
            img = detector_obj.ip_cam_objects[cam].read_single_frame()
            # change from png to jpg to reduce load times
            buff = cv2.imencode(".jpg", img)[1]
            images.append(InputMediaPhoto(io.BytesIO(buff)))
        context.bot.send_media_group(chat_id=update.effective_chat.id, media=images)


def stats(update, context):
    """Send some brief stats, when the command /stats is issued"""
    # TODO


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, hello")


def send_message(bot, chat_id, message, silent=False):
    bot.send_message(chat_id=chat_id, text=message, disable_notification=silent)


def send_photo(bot, chat_id, photo, silent=False):
    bot.send_photo(chat_id=chat_id, photo=photo, disable_notification=silent)


def send_video(bot, chat_id, video, silent=False):
    bot.send_message(chat_id=chat_id, text=message, disable_notification=silent)


def idk(frame=None, thresh=None):
    text = f'Motion detected at {datetime.now().strftime("%m-%d-%Y--%H-%M-%S")}'
    # Convert cv2 image to format usable by telegram
    img = cv2.imread("images/sample_image2.png")
    # img = get_padding_detection(frame, thresh)
    buffer = cv2.imencode(".jpg", img)[1]
    io_buf = io.BytesIO(buffer)

    bot.send_photo(
        chat_id=chat_id, photo=io_buf, caption=text, disable_notification=silent
    )


def poll(detector_obj):
    logging.info("Starting telegram bot")
    # Handle all the user commands
    updater = Updater(token=detector_obj.telegram_token, use_context=True)
    dp = updater.dispatcher
    # Add handlers to respond to each command from a user
    dp.add_handler(
        CommandHandler("vacation", partial(vacation_mode, detector_obj=detector_obj))
    )
    dp.add_handler(
        CommandHandler("view", partial(view_frames, detector_obj=detector_obj))
    )
    dp.add_handler(CommandHandler("stats", stats))

    # Poll/check for commands from the user
    updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    # updater.idle()


# if __name__ == "__main__":
#     config_dict = utils.load_config()

#     telegram_token = config_dict["telegram_token"]
#     people = config_dict["people"]  # Dict of people
#     karsten = people["Karsten"]

#     bot = telegram.Bot(telegram_token)
#     send_photo(bot, karsten, io_buf)
