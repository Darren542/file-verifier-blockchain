// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.28;

contract FileRegistry {
    struct FileInfo {
        string fileName;
        string hash;
        uint version;
        uint timestamp;
    }

    mapping(string => FileInfo[]) private fileVersions;

    event FileVersionAdded(string fileName, string hash, uint version, uint timestamp);

    function addFileVersion(string memory fileName, string memory hash) public {
        uint version = fileVersions[fileName].length + 1;
        fileVersions[fileName].push(FileInfo(fileName, hash, version, block.timestamp));
        emit FileVersionAdded(fileName, hash, version, block.timestamp);
    }

    function getLatestFileVersion(string memory fileName) public view returns (FileInfo memory) {
        require(fileVersions[fileName].length > 0, "File not found");
        return fileVersions[fileName][fileVersions[fileName].length - 1];
    }

    function getAllVersions(string memory fileName) public view returns (FileInfo[] memory) {
        return fileVersions[fileName];
    }
}
