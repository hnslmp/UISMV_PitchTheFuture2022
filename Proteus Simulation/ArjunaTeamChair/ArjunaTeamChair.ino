#include<Servo.h>

Servo backseat;
Servo bottomseat;
Servo bottomheight;
Servo backwidth;

int backpos = 0;
int bottompos = 0;
int backheightpos = 0;
int backwidthpos = 0;

int pos = 0;
int received_data_USB[4];

const unsigned int MAX_MESSAGE_LENGTH = 12;

void setup() {
  Serial.begin(9600);
  backseat.attach(11);
  bottomseat.attach(10);
  bottomheight.attach(9);
  backwidth.attach(6);
  //  received_data_USB[0] = 32;

  for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    backseat.write(pos);              // tell servo to go to position in variable 'pos'
    bottomseat.write(pos);
    bottomheight.write(pos);
    backwidth.write(pos);
    delay(15);                       // waits 15 ms for the servo to reach the position
  }
  for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
    backseat.write(pos);              // tell servo to go to position in variable 'pos'
    bottomseat.write(pos);
    bottomheight.write(pos);
    backwidth.write(pos);
    delay(15);                       // waits 15 ms for the servo to reach the position
  }
  Serial.println("BERHASIL");
}

void loop() {
  //Check to see if anything is available in the serial receive buffer

  while (Serial.available() > 0)
  {
    //Create a place to hold the incoming message
    static char message[MAX_MESSAGE_LENGTH];
    static unsigned int message_pos = 0;

    //Read the next available byte in the serial receive buffer
    char inByte = Serial.read();

    //Message coming in (check not terminating character) and guard for over message size
    if ( inByte != '\n' && (message_pos < MAX_MESSAGE_LENGTH - 1) )
    {
      //Add the incoming byte to our message
      message[message_pos] = inByte;
      message_pos++;
    }
    //Full message received...
    else
    {
      //Add null character to string
      message[message_pos] = '\0';

      //Print the message (or do other things)
      Serial.print("ARDUINO :");
      Serial.println(message);
      //      char buffer[] = "125,256";
      int usbdatalength = 1;
      char delim[] = ",";
      char *ptr = strtok((char*)message, delim);
      char temp[3];
      int temptouint;

      while (ptr != NULL)
      {
        //strcpy(received_data_USB[i],ptr);
        strcpy(temp, ptr);
        sscanf(temp, "%d", &temptouint);
        received_data_USB[usbdatalength - 1] = temptouint;
        ptr = strtok(NULL, delim);
        usbdatalength++;
      }
      if (received_data_USB[0] != 0) {
        backpos = received_data_USB[0];
        bottompos = received_data_USB[1];
        backheightpos = received_data_USB[2];
        backwidthpos = received_data_USB[3];
        Serial.print("BACKPOS :");
        Serial.println(backpos);
        backseat.write(backpos);
        bottomseat.write(bottompos);
        bottomheight.write(backheightpos);
        backwidth.write(backwidthpos);
      }

      /* This loop will show that there are zeroes in the str after tokenizing */
      //      for (int i = 0; i < 2; i++)
      //      {
      //        printf("%d ", received_data_USB[i]); /* Convert the character to integer, in this case
      //                 the character's ASCII equivalent */
      //      }
      //      printf("\n");

      //Reset for the next message
      message_pos = 0;
    }
  }
}
