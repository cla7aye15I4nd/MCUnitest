#include "DueCANLayer.h"

// CAN Layer functions
extern byte canInit(byte cPort, long lBaudRate);
extern byte canTx(byte cPort, long lMsgID, bool bExtendedFormat, byte* cData, byte cDataLen);
extern byte canRx(byte cPort, long* lMsgID, bool* bExtendedFormat, byte* cData, byte* cDataLen);

void Error_Handler(void) {
  while(1);
}

void setup()
{
  // Initialize both CAN controllers
  if(canInit(0, CAN_BPS_250K) != CAN_OK)
    Error_Handler();
  
  if(canInit(1, CAN_BPS_250K) != CAN_OK)
    Error_Handler();
}

void loop()
{
  long lMsgID;
  byte dataLen;
  bool bExtendedFormat;
  
  byte txData[] = {0x01};
  byte rxData[] = {0x01};
  
  if(canTx(0, 0x18FAFE80, true, txData, 1) != CAN_OK)
    Error_Handler();
  
  if(canRx(1, &lMsgID, &bExtendedFormat, &rxData[0], &dataLen) != CAN_OK)
    Error_Handler();

  while(1) {}
}
