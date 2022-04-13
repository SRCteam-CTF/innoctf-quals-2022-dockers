#include "./Dispenser.hpp"

Dispenser::Dispenser (money_pack pack) {
    this->give_pack = pack;
    money_pack pack_;
    pack_.two_thousand = 0;
    pack_.five_thousand = 0;
    pack_.ten_thousand = 0;
    pack_.twenty_thousand = 0;
    this->take_pack = pack_;
}

money_pack Dispenser::pop_money (int num) {
    if (this->give_pack_empty){
        throw DISP_INSUFFICIENT_FUNDS();
    }
    if ((num % 2000 != 0 && num % 5000 != 0 && (num - 5000) % 2000 != 0) || num < 0 || num > MAX_AMOUNT){
        throw DISP_IMPOSSIBLE_WITHDRAWAL();
    }
    int num_twenty_thousand = (int)(num / 20000);
    num %= 20000;
    int num_ten_thousand = (int)(num / 10000);
    num %= 10000;
    int num_five_thousand = (int)(num / 5000);
    num %= 5000;
    int num_two_thousand = (int)(num / 2000);
    if (this->give_pack.twenty_thousand - num_twenty_thousand < 0 ||
        this->give_pack.ten_thousand - num_ten_thousand < 0 ||
        this->give_pack.five_thousand - num_five_thousand < 0 ||
        this->give_pack.two_thousand - num_two_thousand <= 0){
            throw DISP_INSUFFICIENT_FUNDS();
    }
    this->give_pack.twenty_thousand -= num_twenty_thousand;
    this->give_pack.ten_thousand -= num_ten_thousand;
    this->give_pack.five_thousand -= num_five_thousand;
    this->give_pack.two_thousand -= num_two_thousand;
    if (get_pack_balance(this->give_pack) < 2001) {
        this->give_pack_empty = true;
    }
    money_pack out;
    out.twenty_thousand = num_twenty_thousand;
    out.ten_thousand = num_ten_thousand;
    out.five_thousand = num_five_thousand;
    out.two_thousand = num_two_thousand;
    return out;
}

void Dispenser::push_money (int num){
    if (this->take_pack_full == true){
        throw DISP_PACK_FULL();
    }
    if ((num % 2000 != 0 && num % 5000 != 0 && (num - 5000) % 2000 != 0) || num < 0 || num > MAX_AMOUNT){
        throw DISP_IMPOSSIBLE_DEPOSIT();
    }
    int num_twenty_thousand = (int)(num / 20000);
    num %= 20000;
    int num_ten_thousand = (int)(num / 10000);
    num %= 10000;
    int num_five_thousand = (int)(num / 5000);
    num %= 5000;
    int num_two_thousand = (int)(num / 2000);
    if (this->take_pack.twenty_thousand > MAX_PACK_SIZE - num_twenty_thousand ||
        this->take_pack.ten_thousand > MAX_PACK_SIZE - num_ten_thousand ||
        this->take_pack.five_thousand > MAX_PACK_SIZE - num_five_thousand ||
        this->take_pack.two_thousand > MAX_PACK_SIZE - num_two_thousand) {
            throw DISP_PACK_FULL();
    }
    this->take_pack.twenty_thousand += num_twenty_thousand;
    this->take_pack.ten_thousand += num_ten_thousand;
    this->take_pack.five_thousand += num_five_thousand;
    this->take_pack.two_thousand += num_two_thousand;
    if (get_pack_balance(this->take_pack) > MAX_PACK_SIZE * (20000 + 10000 + 5000 + 2000) - 2001) {
        this->take_pack_full = true;
    }
}

std::string Dispenser::grab_secret() {
    return this->secret;
}

int get_pack_balance(money_pack pack){
    return pack.two_thousand * 2000 + pack.five_thousand * 5000 + pack.ten_thousand * 10000 + pack.twenty_thousand * 20000;
}