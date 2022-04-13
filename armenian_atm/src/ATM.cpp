#include "./ATM.hpp"

unsigned char rot8(unsigned char x, int n){
    return (unsigned char)((unsigned char)((x >> n)&0xff) | (unsigned char)((x << (8-n))&0xff));
}

ATM::ATM(money_pack pack, card new_card) : Dispenser(pack){
    srand(time(0));
    user_card = new_card;
    maintenance_mode = false;
    vector<unsigned char> tmp;

    for (int i = 0; i < 33; i++){
        unsigned char x = rand() % 256;
        tmp.push_back(x);
    }

    for (int i = 0; i < 33; i+=3){
        int n1 = (tmp[i] >> 2) & 63;
        int n2 = ((tmp[i] & 3) << 4) | ((tmp[i+1] >> 4) & 15);
        int n3 = ((tmp[i+1] & 15) << 2) | ((tmp[i+2] >> 6) & 3);
        int n4 = tmp[i+2] & 63;
        code += alphabet[n1];
        code += alphabet[n2];
        code += alphabet[n3];
        code += alphabet[n4];
    }
}

vector<unsigned char> ATM::generate_session() {
    unsigned int coeff = -1;
    for (int i = 0; i < 16; i++){
        coeff |= (this->user_card.card_number[i] - '0') + this->user_card.pin[i % 4] * 1337;
    }
    for (int i = 0; i < 8; i++){
        session_key.push_back((rand() % 256) ^ ((coeff >> (i % 4)) && 0xff));
    }
    return session_key;
}

void ATM::take_money(vector<unsigned char> session_key, int num) {
    if (session_key != this->session_key){
        throw ATM_WRONG_SESSION();
    }
    if (this->user_card.balance > MAX_CARD_BALANCE - num) {
        throw ATM_CARD_EXCEPTION();
    }
    this->user_card.balance += num;
    this->push_money(num);
    if (this->give_pack_empty && this->take_pack_full) {
        this->maintenance_mode = true;
    }
}

void ATM::give_money(vector<unsigned char> session_key, int num){
    if (session_key != this->session_key){
        throw ATM_WRONG_SESSION();
    }
    if (this->user_card.balance - num < 0){
        throw ATM_CARD_EXCEPTION();
    }
    this->user_card.balance -= num;
    money_pack out = this->pop_money(num);
    cout << "Your money:" << endl;
    for (int i = 0; i < out.five_thousand + out.ten_thousand + out.twenty_thousand + out.two_thousand; i++){
        cout << "֏";
    }
    cout << endl;

    if (this->give_pack_empty && this->take_pack_full) {
        this->maintenance_mode = true;
    }
}

int ATM::get_card_balance(){
    return this->user_card.balance;
}

void ATM::await_maintenance(){
    cout << "ATM is under maintenance. Please, tell administrator to check it" << endl;
    cout << "Enter the maintenance code: ";
    string code;
    int counter = 0;
    cin >> code;
    counter++;
    while (this->code != code) {
        if (counter == 3){
            cout << "Incorrect code. Turning off." << endl;
            return;
        }
        cout << "Incorrect code. Try again: ";
        cin >> code;
        counter++;
    }
    cout << "You got it. Your secret: " << grab_secret() << endl;
}