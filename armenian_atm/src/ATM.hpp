#include <vector>
#include <iostream>
#include <time.h>

#include "./Dispenser.hpp"

using namespace std;

struct card {
    string card_number;
    vector<int> pin;
    int balance;
};

unsigned char rot8(unsigned char x);
const string alphabet = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890+/";

const int MAX_CARD_BALANCE = 1000000;

class ATM : protected Dispenser {
private:
    vector<unsigned char> session_key;
    card user_card;
    string code;
public:
    bool maintenance_mode;
    ATM(money_pack pack, card new_card);
    vector<unsigned char> generate_session();
    void give_money(vector<unsigned char> session_key, int num);
    void take_money(vector<unsigned char> session_key, int num);
    int get_card_balance();
    void await_maintenance();
};