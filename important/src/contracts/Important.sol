// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

import "./Decryptor.sol";

contract Important {
  address public owner;
  uint256 private key;
  uint256[] private data = new uint256[](32);
  uint256 private counter = 0;

  constructor(uint256 k) {
    owner = msg.sender;
    key = k;
  }

  function add(uint256 m) public {
    require(msg.sender == owner, "Only owner can call the function");
    require(counter < 32, "Data full");
    data[counter] = m;
    counter++;
  }

  function decrypt(address decryptor) public returns(bytes32[] memory) {
    require(msg.sender == owner, "Only owner can call the function");
    Decryptor dec = Decryptor(decryptor);
    uint256 iv = 2 ** 256 - 1;
    for (uint i = 0; i < counter; i++){
      uint256 tmp = data[i];
      data[i] = dec.decrypt(data[i], key, iv);
      iv = tmp;
    }
    bytes32[] memory data_ = get_data();
    counter = 0;
    return data_;
  }

  function get_data() public view returns(bytes32[] memory) {
    bytes32[] memory data_ = new bytes32[](32);
    for (uint i = 0; i < counter; i++){
      data_[i] = bytes32(data[i]);
    }
    return data_;
  }
}
