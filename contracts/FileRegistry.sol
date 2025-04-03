// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.28;

contract FileRegistry {
    struct FileInfo {
        string fileName;
        string hash;
        uint version;
        uint timestamp;
    }
    
    struct FileRecord {
        address owner;
        FileInfo[] versions;
    }
    
    mapping(string => FileRecord) private files;

    event FileVersionAdded(
        string indexed fileName,
        string hash,
        uint version,
        uint timestamp,
        address uploader
    );
    
    event OwnershipTransferred(
        string indexed fileName,
        address indexed previousOwner,
        address indexed newOwner
    );
    
    /**
     * Adds a new file version.
     * - If the file is new, msg.sender becomes the owner.
     * - If the file exists, only the owner can add a new version.
     */
    function addFileVersion(string memory fileName, string memory hash) public {
        FileRecord storage record = files[fileName];
        
        // If no versions exist, initialize and set msg.sender as owner.
        if(record.versions.length == 0) {
            record.owner = msg.sender;
        } else {
            require(record.owner == msg.sender, "Only the file owner can add new versions");
        }
        
        uint newVersion = record.versions.length + 1;
        record.versions.push(FileInfo({
            fileName: fileName,
            hash: hash,
            version: newVersion,
            timestamp: block.timestamp
        }));
        
        emit FileVersionAdded(fileName, hash, newVersion, block.timestamp, msg.sender);
    }
    
    /**
     * Transfers ownership of the file to a new address.
     * Only the current owner can transfer ownership.
     */
    function transferOwnership(string memory fileName, address newOwner) public {
        FileRecord storage record = files[fileName];
        require(record.versions.length > 0, "File not found");
        require(record.owner == msg.sender, "Only the file owner can transfer ownership");
        require(newOwner != address(0), "New owner cannot be the zero address");
        
        address previousOwner = record.owner;
        record.owner = newOwner;
        
        emit OwnershipTransferred(fileName, previousOwner, newOwner);
    }
    
    /**
     * Returns the latest file version info.
     */
    function getLatestFileVersion(string memory fileName) public view returns (FileInfo memory) {
        FileRecord storage record = files[fileName];
        require(record.versions.length > 0, "File not found");
        return record.versions[record.versions.length - 1];
    }
    
    /**
     * Returns all versions of a file.
     */
    function getAllVersions(string memory fileName) public view returns (FileInfo[] memory) {
        return files[fileName].versions;
    }
    
    /**
     * Returns the owner of a file.
     */
    function getOwner(string memory fileName) public view returns (address) {
        FileRecord storage record = files[fileName];
        require(record.versions.length > 0, "File not found");
        return record.owner;
    }
}
