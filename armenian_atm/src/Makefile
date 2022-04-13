CXX=g++
CXXFLAGS=
TARGET_DIR=build
OBJ=$(TARGET_DIR)/ATM.o $(TARGET_DIR)/Dispenser.o $(TARGET_DIR)/main.o $(TARGET_DIR)/Storage.o
FLAG=flag.txt

default: atm

atm: $(OBJ)
	$(CXX) $(CXXFLAGS) -o $(TARGET_DIR)/atm $(OBJ)
	$(RM) $(TARGET_DIR)/*.o
	cp $(FLAG) $(TARGET_DIR)

$(TARGET_DIR)/main.o: main.cpp ATM.hpp
	$(CXX) $(CXXFLAGS) -c main.cpp -o $(TARGET_DIR)/main.o

$(TARGET_DIR)/ATM.o: ATM.cpp ATM.hpp Dispenser.hpp
	$(CXX) $(CXXFLAGS) -c ATM.cpp -o $(TARGET_DIR)/ATM.o

$(TARGET_DIR)/Dispenser.o: Dispenser.cpp Dispenser.hpp Storage.hpp
	$(CXX) $(CXXFLAGS) -c Dispenser.cpp -o $(TARGET_DIR)/Dispenser.o

$(TARGET_DIR)/Storage.o: Storage.cpp Storage.hpp Exceptions.hpp
	$(CXX) $(CXXFLAGS) -c Storage.cpp -o $(TARGET_DIR)/Storage.o

clean:
	$(RM) $(TARGET_DIR)/atm $(TARGET_DIR)/*.o
