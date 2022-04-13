// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract Decryptor {
  address owner;

  constructor(address creator) {
    owner = creator;
  }

  function decrypt(uint256 data, uint256 key, uint256 prev) public view returns (uint256){
    require(msg.sender == owner);
    uint256 a = 0x13371337133713371337133713371337;
    uint256 b = 0x37133713371337133713371337133713;
    assembly {
      let p1 := shr(128, and(prev, 0xffffffffffffffffffffffffffffffff00000000000000000000000000000000))
      let p2 := and(prev, 0xffffffffffffffffffffffffffffffff)
      let z1 := and(data, 0xffffffffffffffffffffffffffffffff)
      let z2 := shr(128, and(data, 0xffffffffffffffffffffffffffffffff00000000000000000000000000000000))
      z1 := xor(z1, p1)
      z2 := xor(z2, p2)

      let k1 := shr(128, and(key, 0xffffffffffffffffffffffffffffffff00000000000000000000000000000000))
      let k2 := and(key, 0xffffffffffffffffffffffffffffffff)
      let y1 := xor(z2, k1)
      let y2 := xor(z1, k2)

      let x1 := xor(y2, a)
      let x2 := xor(y1, b)

      let result := or(shl(128, x1), x2)
      mstore(0x0, result)
      return(0x0, 32)
    }
  }
}
