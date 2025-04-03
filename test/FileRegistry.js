const { expect } = require("chai");

describe("FileRegistry - Basic Tasks", function () {
  let FileRegistry, registry;

  beforeEach(async function () {
    FileRegistry = await ethers.getContractFactory("FileRegistry");
    registry = await FileRegistry.deploy();
    // await registry.deployed();
  });

  it("should add and retrieve the latest file version", async function () {
    const filename = "example.txt";
    const hash1 = "abc123";

    await registry.addFileVersion(filename, hash1);

    const latest = await registry.getLatestFileVersion(filename);
    expect(latest.fileName).to.equal(filename);
    expect(latest.hash).to.equal(hash1);
    expect(latest.version).to.equal(1);
  });

  it("should increment version when a file is updated", async function () {
    const filename = "example.txt";
    const hash1 = "abc123";
    const hash2 = "def456";

    await registry.addFileVersion(filename, hash1);
    await registry.addFileVersion(filename, hash2);

    const latest = await registry.getLatestFileVersion(filename);
    expect(latest.hash).to.equal(hash2);
    expect(latest.version).to.equal(2);
  });

  it("should return all versions", async function () {
    const filename = "example.txt";
    const hash1 = "abc123";
    const hash2 = "def456";

    await registry.addFileVersion(filename, hash1);
    await registry.addFileVersion(filename, hash2);

    const allVersions = await registry.getAllVersions(filename);
    expect(allVersions.length).to.equal(2);
    expect(allVersions[0].hash).to.equal(hash1);
    expect(allVersions[1].hash).to.equal(hash2);
  });

  it("should fail when retrieving a file that does not exist", async function () {
    await expect(
      registry.getLatestFileVersion("nonexistent.txt")
    ).to.be.revertedWith("File not found");
  });
});

describe("FileRegistry - Ownership and Version Control", function () {
  let registry, owner, user1, user2;

  beforeEach(async function () {
    const FileRegistry = await ethers.getContractFactory("FileRegistry");
    [owner, user1, user2] = await ethers.getSigners();
    registry = await FileRegistry.deploy();
    await registry.waitForDeployment();
  });

  it("should allow a user to add a new file and become its owner", async function () {
    await registry.connect(user1).addFileVersion("test.txt", "hash1");
    const fileOwner = await registry.getOwner("test.txt");
    expect(fileOwner).to.equal(user1.address);
  });

  it("should not allow non-owners to add new versions", async function () {
    await registry.connect(user1).addFileVersion("test.txt", "hash1");

    await expect(
      registry.connect(user2).addFileVersion("test.txt", "hash2")
    ).to.be.revertedWith("Only the file owner can add new versions");
  });

  it("should allow owner to add multiple versions", async function () {
    await registry.connect(user1).addFileVersion("test.txt", "hash1");
    await registry.connect(user1).addFileVersion("test.txt", "hash2");

    const latest = await registry.getLatestFileVersion("test.txt");
    expect(latest.version).to.equal(2);
    expect(latest.hash).to.equal("hash2");
  });

  it("should allow the owner to transfer ownership", async function () {
    await registry.connect(user1).addFileVersion("test.txt", "hash1");
    await registry.connect(user1).transferOwnership("test.txt", user2.address);

    const newOwner = await registry.getOwner("test.txt");
    expect(newOwner).to.equal(user2.address);
  });

  it("should not allow non-owners to transfer ownership", async function () {
    await registry.connect(user1).addFileVersion("test.txt", "hash1");

    await expect(
      registry.connect(user2).transferOwnership("test.txt", user2.address)
    ).to.be.revertedWith("Only the file owner can transfer ownership");
  });

  it("should prevent setting ownership to the zero address", async function () {
    await registry.connect(user1).addFileVersion("test.txt", "hash1");

    await expect(
      registry.connect(user1).transferOwnership("test.txt", ethers.ZeroAddress)
    ).to.be.revertedWith("New owner cannot be the zero address");
  });
});

