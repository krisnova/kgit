# kgit
Commonly used git convenience functionality for today's modern developer.

# Installing

##### OSx and Linux only

    pip install kgit

# Enforcing commit username and email by remote host

### Add your workspaces

    kgit workspaces add <workspace>

 - **Workspace** This is a directory that contains git repositories. Usually something like `~/workspace`

### Add github profiles

    kgit profiles add <host> <user> <email>

 - **Host** This is the hostname of your git server. Usually something like `github.com`
 - **User**  This is the name you want associated with your commits. `Kris Childress`
 - **Email** This is the email you want associated with your commits. `kris@nivenly.com`

**Note**: If you forget the syntax just run `kgit profiles add` and you will be prompted.

Newly added repositories are **always** automatically enforced. Meaning that **if this is your first time setting up kgit you are now finished with the setup process and ready to start coding**

# Manual Enforcement

After a user makes a change in the `kgit` configurations, existing git repositories will need to be enforced.

    kgit enforce

All **newly** created repositories will automatically be enforced with the current `kgit` configuration


# kgit and git
The tool will wrap whatever version of `git` you have natively installed. Only some functionality is overridden, and the functionality that is overridden is for convenienve only.

The core library of `kgit` is still `git`. The user will see no discrepancies between the two tools, and in most cases kgit will just pass all of it's arguments to your core `git` program.

The tool offers convenience, reminders, and suggestions. It will not change how `git` operates.

### For example

If we define a new profile for all **github.com** repositories.

    kgit add profile github.com "Kris Childress" kris@nivenly.com

We can now `kgit profiles` to show our current configs. We can see what we have defined already.

    kgit :  ===============================================
    kgit :  ******     Current Git Config Profile     *****
    kgit :  ===============================================
    kgit :  Name  : Charlie Childress
    kgit :  Email : charlie@nivenly.com
    kgit :
    kgit :  ===============================================
    kgit :  ******     Current Registered Profiles    *****
    kgit :  ===============================================
    kgit :  Host  : github.com
    kgit :  Name  : Kris Childress
    kgit :  Email : kris@nivenly.com
    kgit :  ===============================================


Note that there is a discrepancy between our current .gitconfig and our newly created profile for **github.com**

Lets enforce our newly created profile with `kgit enforce`

Now, in a repository **repo_1** with a remote **https://github.com/user/repo_1** we try to make a commit with our bad global .gitconfig

    git commit -m "My commit message"

And we will see the commit will be interrupted

    kgit :  ===========================================================================================
    kgit :  [kgit] v1.0.0
    kgit :  This pre-commit hook is located in /Users/kris/workspace/repo_1/.git/hooks
    kgit :  Running in kgit managed repository
    kgit :  Invalid Username/Email configuration!
    kgit :  ----------------------------------------------------
    kgit :  | Current   : Charlie Childress charlie@nivenly.com
    kgit :  | Expecting : Kris Childress kris@nivenly.com
    kgit :  ----------------------------------------------------
    kgit :  Found matching profile: github.com
    Switch profiles? [y/n]: y
    kgit :  Profile updated. You can now try to commit again.
    kgit :  Invalid commit..
    kgit :  ===========================================================================================

In this case `kgit` found a profile that would work and suggested the change. The user can choose to accept the change or not. If the user decides to use the suggested profile, the user will need to issue a 2nd commit as this commit will inevitably fail.

    git commit -m "My commit message"

And now we will see a successful commit, with our enforced `kgit profile`. The commit will have the user and email we are defined in the **github.com** profile.



