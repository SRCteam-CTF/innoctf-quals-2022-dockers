const Decryptor = artifacts.require('Decryptor')

contract('Decryptor', accounts => {
        it('return value from decrypt is correct', () => {
            let data = web3.utils.toBN('0x3b82e2026e68994113aa156ce730957d18003c7705388021301764ec3399bebf');
            let key =  web3.utils.toBN('0xbb5d75b895f628f2922badb05da83cffb5bab1cd888417a5ecefe37b9e250d03');
            let prev = web3.utils.toBN('0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff');
            let dec;
            let answer;

            return Decryptor.deployed()
                .then(instance => {
                        dec = instance;
                        answer = dec.decrypt(data, key, prev);
                        return answer
                })
                .then(decrypted => {
                    assert.equal(decrypted.toString(), web3.utils.toBN('0x4172617261747b4c30306b5f41745f7448335f563372795f496d70307274616e').toString(),
                                'The answer is incorrect');
                });
            });
});
