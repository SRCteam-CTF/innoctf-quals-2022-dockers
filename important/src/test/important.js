const Decryptor = artifacts.require('Decryptor')
const Important = artifacts.require('Important')

contract('Important', async accounts => {
        it('return value from decrypt is correct', async () => {
            let decryptor = await Decryptor.deployed();
            let data1 = web3.utils.toBN('0x89bf655de13c68683a04c36b4392274a1867ee3e008430ce431e4b7537b0eb20');
            let data2 = web3.utils.toBN('0x26142bca2d35de06cf8807d1f9a952fb5b0a56de1147ae21d5a161becaa96ce1');

            const instance = await Important.deployed();
            await instance.add(data1);
            await instance.add(data2);
            let decrypted = await instance.decrypt.call(decryptor.address);

            let check = [
                        '0x4172617261747b4c30306b5f41745f7448335f563372795f496d70307274616e',
                        '0x745f43306e74723463747d000000000000000000000000000000000000000000'
                        ]
            assert.equal(decrypted[0], check[0], 'The first byte32 is incorrect');
            assert.equal(decrypted[1], check[1], 'The second byte32 is incorrect');
        });
});
