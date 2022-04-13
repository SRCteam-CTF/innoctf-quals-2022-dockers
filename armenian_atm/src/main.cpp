#include <locale>
#include "./ATM.hpp"

using namespace std;

int lang = 1;

int get_choice(int num_choices){
    int choice = -1;
    char choice_;
    std::cin  >> choice_;
    choice = choice_ - '0';
    while (!(choice > 0 && choice <= num_choices)) {
        if (lang == 1)
            cout << "Անվավեր մուտքագրում, խնդրում ենք կրկին փորձել: ";
        else
            cout << "Wrong input, try again: ";
        std::cin  >> choice_;
        choice = choice_ - '0';
    }
    return choice;
}

card generate_new_card(int balance) {
    srand(time(0));
    string card_number = "";
    for (int i = 0; i < 16; i++){
        card_number += (char)(rand() % 10 + '0');
    }
    vector<int> pin;
    for (int i = 0; i < 4; i++){
        pin.push_back(rand() % 10);
    }
    card new_card;
    new_card.card_number = card_number;
    new_card.pin = pin;
    new_card.balance = balance;
    return new_card;
}

void menu() {
    card new_card = generate_new_card(1000000);
    cout << "Your test data:" << endl;
    cout << "Card number - " << new_card.card_number << endl;
    cout << "PIN - " << new_card.pin[0]
                     << new_card.pin[1]
                     << new_card.pin[2]
                     << new_card.pin[3] << endl;
    cout << "Balance - " << new_card.balance << "֏" << endl;
    cout << endl;

    cout << "Բարի գալուստ Լեզուն ընտրելու համար սեղմեք համապատասխան ստեղնը:" << endl;
    cout << "1) Հայերեն" << endl << "2) Անգլերեն" << endl;
    cout << "Ձեր ընտրությունը: ";
    lang = get_choice(2);

    if (lang == 1) {
        cout << "Մուտքագրեք ձեր քարտի համարը: ";
    } else {
        cout << "Enter your card number: ";
    }
    string card_number_;
    std::cin  >> card_number_;
    while (card_number_ != new_card.card_number){
        if (lang == 1){
            cout << "Նման քարտ չի գտնվել!\nՆորից փորձեք: ";
        } else {
            cout << "No such card found!\nTry again: ";
        }
        std::cin  >> card_number_;
    }
    if (lang == 1) {
        cout << "Մուտքագրեք ձեր PIN կոդը: ";
    } else {
        cout << "Enter your PIN: ";
    }
    char pin_[4];
    vector<int> pin__;
    std::cin  >> pin_;
    for (int i = 0; i < 4; i++){
        pin__.push_back(pin_[i] - '0');
    }
    while (pin__ != new_card.pin){
        if (lang == 1) {
            cout << "Սխալ PIN կոդը!\nՆորից փորձեք: ";
        } else {
            cout << "Wrong PIN!\nTry again: ";
        }
        pin__.clear();
        std::cin  >> pin_;
        for (int i = 0; i < 4; i++){
            pin__.push_back(pin_[i] - '0');
        }
    }
    
    money_pack starter_pack;
    starter_pack.twenty_thousand = MAX_PACK_SIZE;
    starter_pack.ten_thousand = MAX_PACK_SIZE;
    starter_pack.five_thousand = MAX_PACK_SIZE;
    starter_pack.two_thousand = MAX_PACK_SIZE;

    ATM atm(starter_pack, new_card);
    vector<unsigned char> session_key = atm.generate_session();
    cout << endl;

    time_t now = time(NULL);
    if (lang == 1){
        cout << "Նոր մուտք. Ընթացիկ ժամանակ:" << asctime(gmtime(&now)) << endl;
    } else {
        cout << "New login. Current time: " << asctime(gmtime(&now)) << endl;
    }

    
    while (true) {
        if (lang == 1) {
            cout << "Ընտրեք գործողություն:" << endl;
            cout << "1) Կանխիկ գումար հանել" << endl
                    << "2) Կանխիկ ավանդ" << endl
                    << "3) Նարդի խաղալ" << endl
                    << "4) Ցույց տալ հավասարակշռությունը" << endl
                    << "5) Ելք" << endl;
        } else {
            cout << "Choose an action:" << endl;
            cout << "1) Withdraw cash" << endl
                    << "2) Deposit cash" << endl
                    << "3) Play nardy" << endl
                    << "4) Show balance" << endl
                    << "5) Exit" << endl;
        }
        int choice = get_choice(5);
        switch (choice) {
            case 1: {
                try {
                    if (lang == 1) {
                        cout << "Մուտքագրեք գումարը: ";
                    } else {
                        cout << "Enter the amount: ";
                    }
                    int amount;
                    std::cin  >> amount;
                    atm.give_money(session_key, amount);
                } catch (ATM_WRONG_SESSION e) {
                    if (lang == 1) {
                        cout << "Սխալ նիստ! Ելք." << endl;
                    } else {
                        cout << "Wrong session! Exit." << endl;
                    }
                    return;
                } catch (DISP_IMPOSSIBLE_WITHDRAWAL e) {
                    if (lang == 1) {
                        cout << "Բանկոմատը չի կարող թողարկել այս գումարը" << endl;
                    } else {
                        cout << "ATM cannot issue this amount" << endl;
                    }
                } catch (DISP_INSUFFICIENT_FUNDS e) {
                    if (lang == 1){
                        cout << "Բանկոմատը անբավարար միջոցներ ունի" << endl;
                    } else {
                        cout << "ATM has insufficient funds" << endl;
                    }
                } catch (ATM_CARD_EXCEPTION e){
                    if (lang == 1){
                        cout << "Դուք չունեք բավարար միջոցներ!" << endl;
                    } else {
                        cout << "You have insufficient funds!" << endl;
                    }
                }
                break;
            }
            case 2: {
                try {
                    if (lang == 1){
                        cout << "Մուտքագրեք գումարը: ";
                    } else {
                        cout << "Enter the amount: ";
                    }
                    int amount;
                    std::cin >> amount;
                    atm.take_money(session_key, amount);
                    cout << "Deposit successful!" << endl;
                } catch (ATM_WRONG_SESSION e) {
                    if (lang == 1) {
                        cout << "Սխալ նիստ! Ելք." << endl;
                    } else {
                        cout << "Wrong session! Exit." << endl;
                    }
                    return;
                } catch (DISP_IMPOSSIBLE_DEPOSIT e) {
                    if (lang == 1) {
                        cout << "Բանկոմատը չի կարող մուտքագրել այս գումարը" << endl;
                    } else {
                        cout << "ATM cannot deposit this amount" << endl;
                    }
                } catch (DISP_PACK_FULL e) {
                    if (lang == 1){
                        cout << "Բանկոմատը լիքն է" << endl;
                    } else {
                        cout << "ATM is full" << endl;
                    }
                } catch (ATM_CARD_EXCEPTION e){
                    if (lang == 1){
                        cout << "Քարտի սահմանաչափը գերազանցում է!" << endl;
                    } else {
                        cout << "Card limit exceed!" << endl;
                    }
                }
                break;
            }
            case 3: {
                if (lang == 1) {
                    cout << "Սա միանգամայն ճիշտ տարբերակ է!\nԿարող եք գնալ https://am.game-game.com/169353/ և խաղալ" << endl;
                } else {
                    cout << "This is absolutely right option!\nYou can go to https://am.game-game.com/169353/ and play" << endl;
                }
                break;
            }
            case 4: {
                if (lang == 1){
                    cout << "Ձեր հաշվեկշիռը: " << atm.get_card_balance() << endl;
                } else {
                    cout << "Your balance: " << atm.get_card_balance() << endl;
                }
                break;
            }
            case 5: {
                if (lang == 1){
                    cout << "Ցտեսություն!" << endl;
                } else {
                    cout << "Bye!" << endl;
                }
                exit(0);
                break;
            }
        }
        if (atm.maintenance_mode) {
            atm.await_maintenance();
            exit(0);
        }
        cout << endl;
    }
}

int main() {
    menu();
    return 0;
}