const Important = artifacts.require("Important");
const Decryptor = artifacts.require("Decryptor");;


module.exports = async (deployer) => {
        /*
  deployer.deploy(Important, '0x0960f2e71aa2d9dbbb857bb7f90a8ec8b5dd63848d38a74a9fe6cce29a0c589c').then(async() => {
          deployer.deploy(Decryptor, Important.address).then(async () => {
            let inst = await Important.deployed();
            await inst.add(web3.utils.toBN('0xe1ff4e79bb2076171d06d134559f664f2a7ae22941822aec17414d0a02a1c720'));
            await inst.add(web3.utils.toBN('0x140927dd6c33c4249bd701aeccb87efb297a49b9252fc26a91d70ee1dca42de4'));
            //let decrypted = await Important.decrypt(Decryptor.address);
          });
  });*/
  await deployer.deploy(Important, '0x0960f2e71aa2d9dbbb857bb7f90a8ec8b5dd63848d38a74a9fe6cce29a0c589c');
  let inst = await Important.deployed();
  await deployer.deploy(Decryptor, inst.address);
  await inst.add(web3.utils.toBN('0xe1ff4e79bb2076171d06d134559f664f2a7ae22941822aec17414d0a02a1c720'));
  await inst.add(web3.utils.toBN('0x140927dd6c33c4249bd701aeccb87efb297a49b9252fc26a91d70ee1dca42de4'));
  let tx = (await inst.decrypt(Decryptor.address)).tx;
  console.log(`Decrypt transaction hash: ${tx}`);
  await inst.add(web3.utils.toBN('0x89bf655de13c68683a04c36b4392274a1867ee3e008430ce431e4b7537b0eb20'));
  await inst.add(web3.utils.toBN('0x26142bca2d35de06cf8807d1f9a952fb5b0a56de1147ae21d5a161becaa96ce1'));
};
