import { Component, OnInit } from '@angular/core';
import { ActionSheetController } from '@ionic/angular';
import { ToastController } from '@ionic/angular';
import { MainControllerService } from '../services/main-controller.service';
import { ModalController } from '@ionic/angular';
import { CartComponent } from '../cart/cart.component';

@Component({
  selector: 'app-tab1',
  templateUrl: './tab1.page.html',
  styleUrls: ['./tab1.page.scss'],
})
export class Tab1Page implements OnInit {

  myCartList: any;
  cartCount: number;
  prodList: any;

  constructor(
    private actionSheetController: ActionSheetController,
    private toastController: ToastController,
    private mainController: MainControllerService,
    private modalController: ModalController,
  ) {
    this.myCartList = [];
    this.prodList = [];
  }

  async presentModalAdd() {
    const modal = await this.modalController.create({
      component: CartComponent,
      componentProps: { cart: this.myCartList }
    });
    modal.onWillDismiss().then(() => {
      location.reload();
    });
    return await modal.present();
  }

  async presentToast(messages: string) {
    const toast = await this.toastController.create({
      message: messages,
      duration: 1000
    });
    toast.present();
  }

  async presentActionSheet(item: object) {
    const actionSheet = await this.actionSheetController.create({
      header: 'Confirm add to cart.',
      buttons: [{
        cssClass: 'custom-success',
        text: 'Yes',
        role: 'destructive',
        icon: 'checkmark-circle-outline',
        handler: () => {
          this.addToCart(item);
        }
      }, {
        text: 'Cancel',
        cssClass: 'custom-danger',
        icon: 'close',
        role: 'cancel',
        handler: () => {
          console.log('Cancel clicked');
        }
      }]
    });
    await actionSheet.present();
  }

  addToCart(cartInfo) {
    if (cartInfo !== null && cartInfo !== undefined) {
      this.myCartList.push(cartInfo)
      this.mainController.initStorage().then(() => {
        this.mainController.addToTemporaryCart(this.myCartList).then(() => {
          this.presentToast(`${cartInfo.ProductName} was added to cart.`);
          this.refreshCartCount();
        });
      }).catch(() => {
        this.presentToast('An error occur');
      });
    }
  }

  refreshCartCount() {
    this.mainController.getCurrentCartContents().then(r => {
      if (r !== null) {
        this.myCartList = r;
        this.cartCount = r.length;
      }
    });
  }

  private getProducts() {
    this.mainController.getProductList().toPromise().then(r => {
      this.prodList = JSON.parse(r);
    });
  }

  ngOnInit() {
    this.getProducts();
    this.mainController.initStorage().then(() => {
      this.refreshCartCount();
    }).catch((e) => {
      console.log(e);
    });
  }
}
