#include <gui/screen1_screen/Screen1View.hpp>
#include "cmsis_os2.h"
#include "main.h"

extern osMessageQueueId_t orderQueueHandle;

Screen1View::Screen1View()
{

}

void Screen1View::setupScreen()
{
    Screen1ViewBase::setupScreen();
}

void Screen1View::tearDownScreen()
{
    Screen1ViewBase::tearDownScreen();
}

void Screen1View::onButtonPressed()
{
    bool startTask = true;  // ค่าที่จะส่งไปยัง Queue
    osMessageQueuePut(orderQueueHandle, &startTask, 0, 0);
}

void Screen1View::updatePredictionLabel(const char* label)
{
    Unicode::strncpy(ch1_menuBuffer, label, CH1_MENU_SIZE);
    ch1_menu.invalidate();
}
