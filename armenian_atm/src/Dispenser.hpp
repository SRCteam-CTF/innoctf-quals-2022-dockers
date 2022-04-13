#include <limits.h>
#include <iostream>
#include <string>

#include "./Storage.hpp"

struct money_pack {
    int two_thousand;
    int five_thousand;
    int ten_thousand;
    int twenty_thousand;
};

const int MAX_PACK_SIZE = 500;
const int MAX_AMOUNT = 1000000;

int get_pack_balance(money_pack pack);

class Dispenser : Storage {
private:
    money_pack give_pack;
    money_pack take_pack;
protected:
    bool give_pack_empty = false;
    bool take_pack_full = false;
    Dispenser(money_pack pack);
    money_pack pop_money(int num);
    void push_money(int num);
    std::string grab_secret();
};