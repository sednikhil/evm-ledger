// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;
contract Ledger {
    struct Entry {
        address user;
        string data;
    }

    Entry[] public ledger;

    event EntryAdded(address indexed user, string data);

    function addEntry(string calldata _data) external {
        require(bytes(_data).length > 0, "Data cannot be empty");
        ledger.push(Entry(msg.sender, _data));
        emit EntryAdded(msg.sender, _data);
    }

    function getEntries() public view returns (Entry[] memory) {
        Entry[] memory entries = new Entry[](ledger.length);
        for (uint i = 0; i < ledger.length; i++) {
            entries[i] = ledger[i];
        }
        return entries;
    }
}
