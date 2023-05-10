from datetime import datetime
import datetime

# Passenger Information
class passengerInfo:
    def __init__(self):
        print("\nPlease enter passenger Information!\n")
        self.name = input("Name: ")
        self.number = int(input("Phone Number: "))
        self.email = input("E-Mail: ")

class main:
    def __init__(self):
        self.bookingNumber = 0
        self.buisnessClass = 0
        self.aClass = 0
        self.economyClass = 0
        self.menu()

    def menu(self):
        print("\n\t_PIA FLIGHT RESERVATION_")
        choice = 'Y'
        while choice != 'E':
            print("\n1. List of Flights")
            print("2. Flight Information")
            print("3. Book Flight")
            print("4. View Booking")
            print("5. Cancel Flight")
            print("6. Search Flight")
            print("7. Search Booking")
            print("8. Create Trip")
            print("9. Cancel Trip")
            self.functions()
            choice = input("\nPress any key to Continue or 'E' to exit: ")
        print("\n\t_THANK YOU_")

    def functions(self):
        choice = input("\n  Enter your choice: ")
        if choice == '1':
            self.listFlights()
        elif choice == '2':
            info = input("\nPlease Enter City or Time to view Information: ")
            self.flightInfo(info.upper())
        elif choice == '3':
            self.bookFlight(passengerInfo(), int(input("\nHow many bookings: ")))
        elif choice == '4':
            self.viewBookingDetails(int(input("\nEnter the Booking Number: ")))
        elif choice == '5':
            self.cancelFlight(int(input("\nEnter the Booking Number: ")))
        elif choice == '6':
            departureCity = input("\nDeparture City: ")
            arrivalCity = input("Arrival City: ")
            self.searchFlight(departureCity.upper(), arrivalCity.upper(), input("Departure Time (Hr:MinAM/PM): "), input("Date (Year/Month/Day): "))
        elif choice == '7':
            self.searchBooking(int(input("\nEnter the Booking Number: ")))
        elif choice == '8':
            self.createTrip()
        elif choice == '9':
            self.cancelTrip()
        else:
            print("\nIncorrect Choice!")
        return

    def header(self):
        flights = open("flights.txt", "r")
        content = ""
        row = 1
        for line in flights:
            if row <= 3:
                content += line
                row += 1
        print(content)
        flights.close()
        return

    def check(self, departure, arrival):
        flights = open("flights.txt", "r")
        flag = False
        for line in flights:
            check = 0
            for word in line.split():
                if word == departure or word == arrival:
                    check += 1
            if check == 2:
                flag = True
        flights.close()
        return flag

    def content(self, fileName):
        readFile = open(fileName, "r")
        if readFile.mode == 'r':
            content = readFile.read()
        readFile.close()
        return content

    def listFlights(self):
        print(self.content("flights.txt"))
        return

    def flightInfo(self, data):
        flights = open("flights.txt", "r")
        check = False
        content = ""
        for line in flights:
            column = 1
            for word in line.split():
                if word == data and (column == 2 or column == 4 or column == 9):
                    content += line
                    check = True
                    break
                column += 1
        if check == False:
            print("\t\nNo Flights!")
            return False
        print("\nAvailable Flights:")
        self.header()
        print(content)
        return

    def bookFlight(self, passenger, number):
        print("\n\t_Booking Flight_")
        for i in range(number):
            # Booking Information
            # City
            departureCity = input("\nCity of Departure: ")
            if self.flightInfo(departureCity) == False:
                print("\nNo Flight from this City!")
                return
            arrivalCity = input("City of Arrival: ")
            # Checking for Flight with these cities
            if self.check(departureCity, arrivalCity) == False:
                print("\nNo Flight available to this city!")
                return
            # Time
            departureTime = input("Departure Time: ")
            date = input("Date: ")
            # Checking for Flight with this timing
            if self.check(departureTime, date) == False:
                print("\n No Flight from", departureCity, "to", arrivalCity, "in this Time!")
                return
            flightNo = self.searchFlight(departureCity, arrivalCity, departureTime, date)
            flights = open("flights.txt", "r")
            flag = False
            if flights.mode == 'r':
                for line in flights:
                    column = 1
                    for word in line.split():
                        if word == flightNo and column == 1:
                            flag = True
                        if flag == True and column == 8:
                            distance = word
                            break
                        column += 1
            flights.close()
            seatInfo = self.seatInfo(distance)
            self.files(passenger, flightNo, seatInfo)
        return

    def files(self, passenger, flightNo, seatInfo):
        flights = open("flights.txt", "r")
        ticket = open("ticket.txt", "w+")
        time = open("time.txt", "a")
        self.bookingNumber = self.bookingNumbers()
        if seatInfo["flag"] == True:
            activeFileName = "reserved.txt"
            print("\nYour Flight has been Reserved!")
        else:
            activeFileName = "bookings.txt"
            print("\nYour Booking Number is =", self.bookingNumber)
            print("\nYour Flight has been Booked!")
        activeFile = open(activeFileName, "a")

        if ticket.mode == 'w+':
            ticket.write("Booking Number: ")
            ticket.write(str(self.bookingNumber))
            ticket.write("\nName: ")
            ticket.write(passenger.name)
            ticket.write("\nNumber: ")
            ticket.write(str(passenger.number))
            ticket.write("\nEmail: ")
            ticket.write(passenger.email)

        if activeFile.mode == 'a':
            activeFile.write(str(self.bookingNumber))
            activeFile.write(" ")
            activeFile.write(passenger.name)
            activeFile.write(" ")
            activeFile.write(str(passenger.number))
            activeFile.write(" ")
            activeFile.write(passenger.email)
            activeFile.write(" ")

        date = datetime.datetime.now()
        if time.mode == 'a':
            time.write(str(self.bookingNumber))
            time.write(" ")
            time.write(str(date.year))
            time.write(" ")
            time.write(str(date.month))
            time.write(" ")
            time.write(str(date.day))
            time.write(" ")
            time.write(str(date.hour))
            time.write(" ")
            time.write(str(date.minute))
            time.write(" ")
            time.write(str(date.second))
            time.write("\n")

        check = False
        if flights.mode == 'r':
            for line in flights:
                column = 1
                for word in line.split():
                    if word == str(flightNo) and column == 1:
                        check = True
                    if check == True:
                        if column == 2:
                            ticket.write("\nCity of Departure: ")
                            ticket.write(word)
                            activeFile.write(word)
                            activeFile.write(" ")
                        elif column == 3:
                            ticket.write("\nCity of Arrival: ")
                            ticket.write(word)
                            activeFile.write(word)
                            activeFile.write(" ")
                        elif column == 4:
                            ticket.write("\nTime of Departure:\t")
                            ticket.write(word)
                            activeFile.write(word)
                            activeFile.write(" ")
                        elif column == 5:
                            ticket.write("\nTime of Arrival:\t")
                            ticket.write(word)
                            activeFile.write(word)
                            activeFile.write(" ")
                        elif column == 6:
                            ticket.write("\nDuration:\t")
                            ticket.write(word)
                            activeFile.write(word)
                            activeFile.write(" ")
                        elif column == 7:
                            ticket.write("\nType:\t")
                            ticket.write(word)
                            activeFile.write(word)
                            activeFile.write(" ")
                        elif column == 8:
                            ticket.write("\nDistance:\t")
                            ticket.write(word)
                            activeFile.write(word)
                            activeFile.write(" ")
                        elif column == 9:
                            ticket.write("\nDate:\t")
                            ticket.write(word)
                            activeFile.write(word)
                            activeFile.write(" ")
                            ticket.write("\nSeat Type:\t")
                            ticket.write(str(seatInfo["seatType"]))
                            activeFile.write(str(seatInfo["seatType"]))
                            activeFile.write(" ")
                            ticket.write("\nPrice:\t")
                            ticket.write(str(seatInfo["price"]))
                            activeFile.write(str(seatInfo["price"]))
                            activeFile.write(" ")
                            ticket.write("\nAge:\t")
                            ticket.write(str(seatInfo["age"]))
                            activeFile.write(str(seatInfo["age"]))
                            if activeFileName == "bookings.txt":
                                activeFile.write(" ")
                            if activeFileName == "reserved.txt":
                                activeFile.write("\n")
                            ticket.write("\nSeat Number:\t")
                            ticket.write(str(seatInfo["seatNo"]))
                            if activeFileName == "bookings.txt":
                                activeFile.write(str(seatInfo["seatNo"]))
                                activeFile.write("\n")
                            if seatInfo["flag"] == True:
                                ticket.write("\nReserved:\t")
                                ticket.write(str(seatInfo["flag"]))
                    column += 1
                if check == True:
                    break
        flights.close()
        activeFile.close()
        ticket.close()
        time.close()
        return

    def seatInfo(self, distance):
        age = int(input("Age: "))
        print("\t_SEAT TYPE_")
        print(" 1. Business class")
        print(" 2. A class")
        print(" 3. Economy class\n")
        seatType = int(input("Type: "))
        flag = False
        check = False
        while flag == False:
            if seatType == 1:
                price = 15 * int(distance)
                seatNo = self.seats(1)
                if self.buisnessClass <= 10:
                    self.buisnessClass += 1
                    check = True
                else:
                    print("\nBuisness Class seats are full!")
                    flag = True
            elif seatType == 2:
                seatNo = self.seats(2)
                price = 25 * int(distance)
                if self.aClass <= 20:
                    self.aClass += 1
                    check = True
                else:
                    print("\nA Class seats are full!")
                    flag = True
            elif seatType == 3:
                seatNo = self.seats(3)
                price = 35 * int(distance)
                if self.economyClass <= 170:
                    self.economyClass += 1
                    check = True
                else:
                    print("\nEconomy Class seats are full!")
                    flag = True
            else:
                print("Incorrect Choice!!!")
                seatType = int(input("\nType: "))
                continue

            totalSeats = self.buisnessClass + self.aClass + self.economyClass
            if totalSeats > 200:
                print("All class seats are full!")
                flag = True
                break

            if flag == True:
                while 1:
                    choice = input(
                        "\nReserve your seat in this class? (Y)\nCheck for other class seat? (N)\n\tChoice: ")
                    if choice == 'Y':
                        check = True
                        break
                    elif choice == 'N':
                        seatType = int(input("\nType: "))
                        flag = False
                        break
                    else:
                        print("\nIncorrect choice!")
            if check == True:
                break

        if age < 12:
            price = age * (price * 0.75)
        seatInfo = {
            "flag": flag,
            "seatType": seatType,
            "age": age,
            "price": price,
            "seatNo": seatNo
        }
        return seatInfo

    def seats(self, seatType):
        seats = open("seats.txt", "r")
        if seats.mode == 'r':
            content = seats.readlines()
        seats.close()
        seats = open("seats.txt", "w+")
        if seats.mode == 'w+':
            row = 1
            for line in content:
                if seatType == 1 and row == 1:
                    if int(line) <= 10:
                        line = str((int(line) + 1)) + "\n"
                    self.buisnessClass = int(line)
                    seatNo = str(self.buisnessClass) + "B"
                elif seatType == 2 and row == 2:
                    if int(line) <= 20:
                        line = str((int(line) + 1)) + "\n"
                    self.aClass = int(line)
                    seatNo = str(self.aClass) + "A"
                elif seatType == 3 and row == 3:
                    if int(line) <= 170:
                        line = str((int(line) + 1)) + "\n"
                    self.economyClass = int(line)
                    seatNo = str(self.economyClass) + "E"
                if row == 1:
                    seats.write(line)
                elif row == 2:
                    seats.write(str(line))
                elif row == 3:
                    seats.write(str(line))
                row += 1
        seats.close()
        return seatNo

    def bookingNumbers(self):
        bookingFile = open("bookingNumber.txt", "r")
        if bookingFile.mode == 'r':
            bookingNo = bookingFile.read()
        bookingFile.close()
        bookingFile = open("bookingNumber.txt", "w+")
        if bookingFile.mode == 'w+':
            bookingFile.write(str(int(bookingNo) + 1))
        bookingFile.close()
        return int(bookingNo)

    def viewBookingDetails(self, bookingNo):
        booking = open('bookings.txt', 'r')
        check = False
        for line in booking:
            column = 1
            for word in line.split():
                if word == str(bookingNo) and column == 1:
                    print("\nBooking Number:", word)
                    check = True
                if check == True:
                    if column == 2:
                        print("Name:", word)
                    if column == 3:
                        print("Number:", word)
                    if column == 4:
                        print("E-Mail:", word)
                    if column == 5:
                        print("Departure City:", word)
                    if column == 6:
                        print("Arrival City:", word)
                    if column == 7:
                        print("Departure Time:", word)
                    if column == 8:
                        print("Arrival Time:", word)
                    if column == 9:
                        print("Duration:", word, " Hrs")
                    if column == 10:
                        print("Flight Type:", word)
                    if column == 11:
                        print("Distance:", word, " Km")
                    if column == 12:
                        print("Date:", word)
                    if column == 13:
                        print("Seat Type:", word)
                    if column == 14:
                        print("Price:", word, "Rs")
                    if column == 15:
                        print("Age:", word, "Yrs")
                    if column == 16:
                        print("Seat Number:", word)
                    column += 1
            if check == True:
                break
        if check == False:
            print("No Booking with this Number!")

    def searchFlight(self, departureCity, arrivalCity, departureTime, date):
        flights = open("flights.txt", "r")
        flag = False
        for line in flights:
            column = 1
            check = 0
            for word in line.split():
                if column == 1:
                    number = word
                if word == departureCity or word == arrivalCity or word == departureTime or word == date:
                    check += 1
                column += 1
            if check == 4:
                self.header()
                print(line)
                flightNo = number
                flag = True
                break
        flights.close()
        if flag == True:
            return flightNo
        print("\nNo Flight with this Information!")

    def searchBooking(self, bookingNo):
        bookings = open("bookings.txt", "r")
        flag = False
        for line in bookings:
            column = 0
            for word in line.split():
                if word == str(bookingNo) and column == 0:
                    flag = True
                column += 1
        bookings.close()
        if flag == True:
            print("\nBooking Found!")
        else:
            print("\nNo Booking with this Number!")
        return

    def cancelFlight(self, bookingNo):
        time = open("time.txt", "r")
        bookings = open("bookings.txt", "r")
        if bookings.mode == 'r':
            content = bookings.readlines()
        bookings.close()
        booking = open("bookings.txt", "w+")
        check = False
        for line in content:
            column = 1
            for word in line.split():
                if column == 1:
                    if word != str(bookingNo):
                        booking.write(line)
                        break
                    else:
                        check = True
                if check == True:
                    if column == 7:
                        depTime = word
                    if column == 12:
                        depDate = word
                    if column == 14:
                        price = int(word)
                    if column == 16:
                        seatType = word
                column += 1
        if check == False:
            print("\nNo Booking with this Number!")
            return False

        date = datetime.datetime.now()
        # datetime(year, month, day, hour, minute, second)
        cancelTime = datetime.datetime(date.year, date.month, date.day, date.hour, date.minute, date.second)
        departureTime = datetime.datetime(int(depDate[0] + depDate[1] + depDate[2] + depDate[3]),
                                          int(depDate[5] + depDate[6]), int(depDate[8] + depDate[9]),
                                          int(depTime[0] + depTime[1]), int(depTime[3] + depTime[4]), 0)
        difference = departureTime - cancelTime
        hours = (difference.total_seconds() / 60) / 24
        print("\n", hours, "Hours remaining in flight!")
        if hours >= 72:
            print("\nFlight cancelled with 100% price refund =", price, "Rs")
        elif hours >= 48:
            print("Flight cancelled with 75% price refund =", (price * 0.75), "Rs")
        elif hours >= 24:
            print("Flight cancelled with 50% price refund =", (price * 0.50), "Rs")
        elif hours >= 12:
            print("Flight cancelled with 25% price refund =", (price * 0.25), "Rs")
        elif hours < 12:
            print("Flight cancelled with No price refund =", 0, "Rs")

        reserved = open("reserved.txt", "r")
        if reserved.mode == 'r':
            content = reserved.readlines()
        reserved.close()
        if content == "":
            return
        reserved = open("reserved.txt", "w+")
        booking = open("bookings.txt", "a")
        row = 1
        for line in content:
            if row == 1:
                booking.write(line)
            else:
                reserved.write(line)
            row += 1
        reserved.close()
        booking.close()
        return

    def createTrip(self):
        choice = 'A'
        passenger = passengerInfo()
        # Booking Information
        # City
        print("Trip Route: ")
        bookingFile = open("bookingNumber.txt", "r")
        if bookingFile.mode == 'r':
            presentBookingNo = bookingFile.read()
        bookingFile.close()
        while choice != 'F':
            if choice == 'A':
                self.bookFlight(passenger, 1)
            elif choice == 'D':
                print("Enter destination you want to delete: ")
                departureCity = input("Departure City: ")
                booking = open("bookings.txt", "r")
                content = booking.readlines()
                check = False
                for line in content:
                    column = 1
                    for word in line.split():
                        if column == 1:
                            bookingNo = word
                        if word == departureCity and column == 5 and (int(bookingNo) >= int(presentBookingNo)):
                            check = True
                            print(bookingNo)
                            self.cancelFlight(bookingNo)
                        column += 1
                    if check == True:
                        break
                if check == False:
                    print("\nNo City Found in the Trip!\n")
            else:
                print("\nIncorrect Choice!!!")
            choice = input("\nEnter 'A' to add 'D' to delete a desination or 'F' to Finalise Trip: ")

    def cancelTrip(self):
        choice = ''
        while choice != 'F':
            bookingNo = input("\nEnter the booking Number against Trip destination: ")
            if self.cancelFlight(bookingNo) == False:
                return
            choice = input("Press any key to cancel another desination or 'F' to Finalise: ")


PIA = main()